#!/usr/bin/env python3

from __future__ import annotations

import argparse
import base64
import io
import json
from dataclasses import dataclass
import os
import time
from typing import Tuple
import numpy as np
import requests
from PIL import Image
import torch
import torch.nn as nn

MNIST_MEAN = 0.1307
MNIST_STD = 0.3081


class SimpleClassifier(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.conv1 = nn.Conv2d(1, 32, 3, 1)
        self.conv2 = nn.Conv2d(32, 64, 3, 1)
        self.dropout1 = nn.Dropout(0.25)
        self.dropout2 = nn.Dropout(0.5)
        self.fc1 = nn.Linear(9216, 128)
        self.fc2 = nn.Linear(128, 10)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.conv1(x)
        x = torch.relu(x)
        x = self.conv2(x)
        x = torch.relu(x)
        x = torch.max_pool2d(x, 2)
        x = self.dropout1(x)
        x = torch.flatten(x, 1)
        x = self.fc1(x)
        x = torch.relu(x)
        x = self.dropout2(x)
        x = self.fc2(x)
        return torch.log_softmax(x, dim=1)


def mnist_normalize(x01: torch.Tensor) -> torch.Tensor:
    return (x01 - MNIST_MEAN) / MNIST_STD


def png_from_x01(x01: np.ndarray) -> str:
    x255 = np.clip((x01 * 255.0).round(), 0, 255).astype(np.uint8)
    img = Image.fromarray(x255, mode="L")
    buf = io.BytesIO()
    img.save(buf, format="PNG", optimize=True)
    return base64.b64encode(buf.getvalue()).decode("ascii")


def x01_from_b64_png(b64: str) -> np.ndarray:
    raw = base64.b64decode(b64)
    img = Image.open(io.BytesIO(raw)).convert("L")
    if img.size != (28, 28):
        raise ValueError("Expected 28x28 PNG")
    x = np.asarray(img, dtype=np.float32) / 255.0
    return np.clip(x, 0.0, 1.0)


@dataclass
class Challenge:
    epsilon: float
    label: int
    sample_index: int
    x01: np.ndarray


def fetch_challenge(host: str, retries: int = 30, delay: float = 1.0) -> Challenge:
    last_err = None
    for _ in range(max(1, retries)):
        try:
            r = requests.get(f"{host}/challenge", timeout=5)
            r.raise_for_status()
            payload = r.json()
            break
        except Exception as e:
            last_err = e
            time.sleep(delay)
    else:
        raise RuntimeError(f"Failed to connect to {host}/challenge: {last_err}") from last_err
    x2d = x01_from_b64_png(payload["image_b64"])
    x4d = x2d[None, None, ...]
    return Challenge(
        epsilon=float(payload["epsilon"]),
        label=int(payload["label"]),
        sample_index=int(payload["sample_index"]),
        x01=x4d.astype(np.float32),
    )


def load_model(weights_path: str) -> SimpleClassifier:
    model = SimpleClassifier()
    state = torch.load(weights_path, map_location=torch.device("cpu"), weights_only=False)
    model.load_state_dict(state)
    model.eval()
    return model


def fgsm_untargeted(model: nn.Module, x01: np.ndarray, y: int, epsilon: float) -> np.ndarray:
    x = torch.from_numpy(x01).float().requires_grad_(True)
    target = torch.tensor([y], dtype=torch.long)
    logits = model(mnist_normalize(x))
    loss = nn.NLLLoss()(logits, target)
    model.zero_grad()
    loss.backward()
    grad_sign = x.grad.detach().sign()
    x_adv = x + epsilon * grad_sign
    x_adv = torch.clamp(x_adv, 0.0, 1.0)
    return x_adv.detach().cpu().numpy()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="http://127.0.0.1:8000")
    parser.add_argument("--weights", default="solver/fgsm_weights.pth")
    args = parser.parse_args()

    chall = fetch_challenge(args.host)
    if not os.path.exists(args.weights):
        os.makedirs(os.path.dirname(args.weights), exist_ok=True)
        wb = requests.get(f"{args.host}/weights", timeout=15).content
        with open(args.weights, "wb") as f:
            f.write(wb)
    model = load_model(args.weights)

    x = torch.from_numpy(chall.x01)
    clean_pred = int(torch.argmax(model(mnist_normalize(x)), dim=1).item())
    if clean_pred != chall.label:
        print(f"Warning: local clean prediction {clean_pred} != label {chall.label}")

    safety = [1.0 / 255.0 + 1e-4, 2e-3, 1e-3, 5e-4, 0.0]
    x_adv = None
    adv_pred = None
    linf = None
    for m in safety:
        eps_eff = max(0.0, chall.epsilon - m)
        cand = fgsm_untargeted(model, chall.x01, chall.label, eps_eff)
        cand_pred = int(torch.argmax(model(mnist_normalize(torch.from_numpy(cand))), dim=1).item())
        if cand_pred != chall.label:
            x_adv = cand
            adv_pred = cand_pred
            linf = float(np.max(np.abs(x_adv - chall.x01)))
            break

    if x_adv is None:
        eps_eff = chall.epsilon * 0.99
        x_adv = fgsm_untargeted(model, chall.x01, chall.label, eps_eff)
        adv_pred = int(torch.argmax(model(mnist_normalize(torch.from_numpy(x_adv))), dim=1).item())
        linf = float(np.max(np.abs(x_adv - chall.x01)))

    print(json.dumps({"linf": linf, "pred": adv_pred, "clean_pred": clean_pred}, indent=2))

    x2d = x_adv[0, 0]
    b64 = png_from_x01(x2d)
    r = requests.post(f"{args.host}/submit", json={"image_b64": b64}, timeout=10)
    try:
        r.raise_for_status()
    except Exception:
        print("Server response:", r.text)
        raise
    print("Flag:", r.json().get("flag"))


if __name__ == "__main__":
    main()

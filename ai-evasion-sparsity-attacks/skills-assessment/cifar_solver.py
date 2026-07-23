#!/usr/bin/env python3
from __future__ import annotations
import argparse, base64, io, json
from dataclasses import dataclass
from typing import Dict, List
import numpy as np
import urllib.request
from PIL import Image
import torch
import torch.nn as nn
import os

CIFAR10_MEAN = (0.4914, 0.4822, 0.4465)
CIFAR10_STD = (0.2470, 0.2435, 0.2616)
SEED = 1337

def set_seed(seed=SEED):
    np.random.seed(seed)
    torch.manual_seed(seed)

def cifar_normalize(x01):
    mean = torch.tensor(CIFAR10_MEAN, dtype=x01.dtype, device=x01.device)[None,:,None,None]
    std = torch.tensor(CIFAR10_STD, dtype=x01.dtype, device=x01.device)[None,:,None,None]
    return (x01 - mean) / std

class BasicBlock(nn.Module):
    expansion = 1
    def __init__(self, in_planes, planes, stride=1):
        super().__init__()
        self.conv1 = nn.Conv2d(in_planes, planes, 3, stride=stride, padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(planes)
        self.conv2 = nn.Conv2d(planes, planes, 3, stride=1, padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(planes)
        self.shortcut = nn.Sequential()
        if stride != 1 or in_planes != planes:
            self.shortcut = nn.Sequential(nn.Conv2d(in_planes, planes, 1, stride=stride, bias=False), nn.BatchNorm2d(planes))
    def forward(self, x):
        out = torch.relu(self.bn1(self.conv1(x)))
        out = self.bn2(self.conv2(out))
        out += self.shortcut(x)
        return torch.relu(out)

class ResNetCIFAR(nn.Module):
    def __init__(self, block=BasicBlock, num_blocks=(2,2,2,2), num_classes=10):
        super().__init__()
        self.in_planes = 64
        self.conv1 = nn.Conv2d(3, 64, 3, stride=1, padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(64)
        self.layer1 = self._make_layer(block, 64, num_blocks[0], 1)
        self.layer2 = self._make_layer(block, 128, num_blocks[1], 2)
        self.layer3 = self._make_layer(block, 256, num_blocks[2], 2)
        self.layer4 = self._make_layer(block, 512, num_blocks[3], 2)
        self.avgpool = nn.AdaptiveAvgPool2d(1)
        self.fc = nn.Linear(512*block.expansion, num_classes)
    def _make_layer(self, block, planes, num_blocks, stride):
        layers = []
        for s in [stride]+[1]*(num_blocks-1):
            layers.append(block(self.in_planes, planes, s))
            self.in_planes = planes*block.expansion
        return nn.Sequential(*layers)
    def forward(self, x):
        out = torch.relu(self.bn1(self.conv1(x)))
        out = self.layer1(out); out = self.layer2(out)
        out = self.layer3(out); out = self.layer4(out)
        out = self.avgpool(out)
        return self.fc(torch.flatten(out, 1))

def _compute_fista_momentum(it):
    return it / (it + 3.0)

def _apply_shrinkage_thresholding(y, original_images, threshold, clip_min=0.0, clip_max=1.0):
    diff = y - original_images
    shrink_positive = torch.clamp(y - threshold, min=clip_min, max=clip_max)
    shrink_negative = torch.clamp(y + threshold, min=clip_min, max=clip_max)
    c1 = (diff > threshold).float()
    c2 = (torch.abs(diff) <= threshold).float()
    c3 = (diff < -threshold).float()
    return c1*shrink_positive + c2*original_images + c3*shrink_negative

def _compute_adversarial_loss(logits, target, confidence):
    target_logit = logits[0, target]
    other_logits = torch.cat([logits[0, :target], logits[0, target+1:]])
    return torch.clamp(torch.max(other_logits) - target_logit + confidence, min=0)

def ead_targeted(model, x01, target, c=0.01, beta=0.01, lr=0.01, max_iter=1000, decision_rule="EN", confidence=0.0):
    set_seed()
    x_orig = x01.detach().clone().float()
    def _run_fista(c_val):
        adv_curr = x_orig.clone()
        y_mom = adv_curr.clone()
        best_local = None
        best_score = float("inf")
        success = False
        const = torch.tensor([c_val], device=x_orig.device, dtype=x_orig.dtype)
        for it in range(max_iter):
            y_mom = y_mom.detach().requires_grad_(True)
            logits = model(cifar_normalize(y_mom))
            adv_loss = _compute_adversarial_loss(logits, target, confidence)
            l2_sq = torch.sum((y_mom - x_orig)**2)
            total = const[0]*adv_loss + l2_sq
            total.backward()
            grad = y_mom.grad
            y_new = y_mom - lr*grad
            adv_new = _apply_shrinkage_thresholding(y_new, x_orig, lr*beta, 0.0, 1.0)
            adv_new = torch.clamp(adv_new, 0.0, 1.0)
            mom = _compute_fista_momentum(it)
            y_mom = torch.clamp(adv_new + mom*(adv_new-adv_curr), 0.0, 1.0)
            adv_curr = adv_new
            with torch.no_grad():
                logits_adv = model(cifar_normalize(adv_new))
                pred = int(torch.argmax(logits_adv, dim=1).item())
                diff = adv_new - x_orig
                l1 = torch.sum(torch.abs(diff)).item()
                l2 = torch.norm(diff.flatten(), p=2).item()
                score = beta*l1+l2 if decision_rule.upper()=="EN" else l1
                if pred == target:
                    success = True
                    if score < best_score:
                        best_score = score
                        best_local = adv_new.clone()
                if it > 100 and pred == target and torch.softmax(logits_adv,dim=1)[0,target].item() > 0.9:
                    break
        return (best_local if best_local is not None else adv_curr).detach(), success, best_score
    low = 0.0; high = None; c_cur = float(c)
    best_overall = x_orig.clone(); best_overall_score = float("inf"); any_success = False
    for _ in range(6):
        cand, ok, score = _run_fista(c_cur)
        if ok:
            any_success = True
            if score < best_overall_score:
                best_overall, best_overall_score = cand.clone(), score
            high = c_cur if high is None else min(high, c_cur)
            c_cur = (low + (high if high is not None else c_cur)) / 2.0
            if high is not None and (high-low) < 1e-4:
                break
        else:
            low = c_cur
            c_cur = c_cur*2.0 if high is None else (low+high)/2.0
            if c_cur > 1.0:
                c_cur = 1.0
    return torch.clamp(best_overall if any_success else cand, 0.0, 1.0).detach()

def jsma_targeted(model, x01, target, theta=0.12, gamma=0.15, max_iter=250, top_k=5):
    set_seed()
    x = x01.detach().clone().float()
    B, C, H, W = x.shape
    pixel_budget = max(1, int(gamma*H*W))
    touched = torch.zeros((H*W,), dtype=torch.bool, device=x.device)
    saturated = torch.zeros((H*W,), dtype=torch.bool, device=x.device)
    touch_counts = torch.zeros((H*W,), dtype=torch.int32, device=x.device)
    x_orig = x.clone()
    AMP_CAP = 0.25; MAX_TOUCHES = 5; MIN_BAND = 0.06; MAX_BAND = 0.94
    top_k = max(1, int(top_k))
    def _at_boundary(v):
        return bool(torch.all((v <= 1e-3) | (v >= 1-1e-3)).item())
    changed_unique = 0; it = 0
    while it < max_iter and changed_unique < pixel_budget:
        it += 1
        x_req = x.detach().clone().requires_grad_(True)
        logits = model(cifar_normalize(x_req))
        pred = int(torch.argmax(logits, dim=1).item())
        if pred == target:
            break
        g_all = torch.autograd.grad(logits[0].sum(), x_req, retain_graph=True)[0]
        g_t = torch.autograd.grad(logits[0, target], x_req, retain_graph=False)[0]
        alpha_pix = g_t.view(C,H,W).sum(dim=0).flatten()
        beta_pix = (g_all-g_t).view(C,H,W).sum(dim=0).flatten()
        available = ~saturated
        inc_valid = (alpha_pix>0)&(beta_pix<0)&available
        dec_valid = (alpha_pix<0)&(beta_pix>0)&available
        if not (inc_valid.any() or dec_valid.any()):
            break
        base_vals = x[0].detach().mean(dim=0).flatten()
        center = 1.0 - torch.clamp(torch.abs(base_vals-0.5)/0.5, 0.0, 1.0)
        inc_raw = torch.zeros_like(alpha_pix); dec_raw = torch.zeros_like(alpha_pix)
        inc_raw[inc_valid] = alpha_pix[inc_valid]*(-beta_pix[inc_valid])
        dec_raw[dec_valid] = (-alpha_pix[dec_valid])*(beta_pix[dec_valid])
        inc_score = inc_raw*center; dec_score = dec_raw*center
        k = min(top_k, pixel_budget-changed_unique)
        scores = []
        if inc_valid.any():
            inc_vals, inc_idx = torch.topk(inc_score, k=min(k, int(inc_valid.sum().item())))
            for s, idx in zip(inc_vals.tolist(), inc_idx.tolist()):
                if s > 0: scores.append((s, idx, +1.0))
        if dec_valid.any():
            dec_vals, dec_idx = torch.topk(dec_score, k=min(k, int(dec_valid.sum().item())))
            for s, idx in zip(dec_vals.tolist(), dec_idx.tolist()):
                if s > 0: scores.append((s, idx, -1.0))
        scores.sort(key=lambda t: t[0], reverse=True)
        scores = scores[:k]
        if not scores:
            if inc_score.max() >= dec_score.max():
                scores = [(float(inc_score.max().item()), int(torch.argmax(inc_score).item()), +1.0)]
            else:
                scores = [(float(dec_score.max().item()), int(torch.argmax(dec_score).item()), -1.0)]
        for _, p_idx, direction in scores:
            if saturated[p_idx]: continue
            r = p_idx//W; c_ = p_idx%W
            before = x[0,:,r,c_].clone()
            mg = (2*g_t-g_all)[0,:,r,c_]
            step_vec = (mg>0).to(x.dtype) if direction>0 else -(mg<0).to(x.dtype)
            if float(step_vec.abs().sum().item()) == 0.0:
                step_vec = torch.full((C,), float(direction), dtype=x.dtype, device=x.device)
            candidate = torch.clamp(x[0,:,r,c_]+theta*step_vec, MIN_BAND, MAX_BAND)
            base = x_orig[0,:,r,c_]
            delta = torch.clamp(candidate-base, min=-AMP_CAP, max=AMP_CAP)
            x[0,:,r,c_] = torch.clamp(base+delta, MIN_BAND, MAX_BAND)
            if not touched[p_idx] and not torch.allclose(before, x[0,:,r,c_]):
                touched[p_idx] = True; changed_unique += 1
            touch_counts[p_idx] += 1
            at_cap = torch.any(torch.isclose(torch.abs(delta), torch.tensor(AMP_CAP, device=x.device, dtype=x.dtype), atol=1e-4))
            if _at_boundary(x[0,:,r,c_]) or at_cap or (touch_counts[p_idx] >= MAX_TOUCHES):
                saturated[p_idx] = True
            if changed_unique >= pixel_budget: break
    return torch.clamp(x, 0.0, 1.0).detach()

def _to_b64_rgb_x01(x4d):
    x = np.transpose(x4d[0], (1,2,0))
    x255 = np.clip((x*255.0).round(), 0, 255).astype(np.uint8)
    img = Image.fromarray(x255, mode="RGB")
    buf = io.BytesIO()
    img.save(buf, format="PNG", optimize=True)
    return base64.b64encode(buf.getvalue()).decode("ascii")

def _x01_from_b64_rgb(b64):
    raw = base64.b64decode(b64)
    img = Image.open(io.BytesIO(raw)).convert("RGB")
    x = np.asarray(img, dtype=np.float32)/255.0
    return np.transpose(x, (2,0,1))[None,...].astype(np.float32)

@dataclass
class ChallengeItem:
    sample_id: int; label: int; target: int; required_method: str; x01: np.ndarray

def _http_get_json(url):
    req = urllib.request.Request(url, method="GET")
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))

def _http_post_json(url, body):
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type":"application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))

def fetch_challenge(host):
    payload = _http_get_json(f"{host}/challenge")
    out = []
    for it in payload["items"]:
        raw = base64.b64decode(it["image_b64"])
        img = Image.open(io.BytesIO(raw)).convert("RGB")
        x = np.transpose(np.asarray(img, dtype=np.float32)/255.0, (2,0,1))[None,...]
        out.append(ChallengeItem(int(it["sample_id"]), int(it["label"]), int(it["target"]), str(it["required_method"]).lower(), x.astype(np.float32)))
    return out

def load_model(weights, device):
    ckpt = torch.load(weights, map_location=device, weights_only=False)
    if isinstance(ckpt, dict) and ("state_dict" in ckpt or "state_dict_ema" in ckpt or "arch" in ckpt):
        model = ResNetCIFAR(block=BasicBlock, num_blocks=(2,2,2,2)).to(device)
        sd = ckpt.get("state_dict_ema") or ckpt.get("state_dict")
        model.load_state_dict(sd)
    else:
        model = ResNetCIFAR(block=BasicBlock, num_blocks=(2,2,2,2)).to(device)
        model.load_state_dict(ckpt)
    return model.eval()

def craft_adv(model, device, item):
    x = torch.from_numpy(item.x01).to(device)
    t = item.target
    if item.required_method == "ead":
        for params in [{"c":0.01,"beta":0.01,"lr":0.01,"max_iter":1000},{"c":0.005,"beta":0.02,"lr":0.01,"max_iter":1200},{"c":0.02,"beta":0.01,"lr":0.005,"max_iter":800}]:
            cand = ead_targeted(model, x, target=t, **params)
            b64 = _to_b64_rgb_x01(cand.detach().cpu().numpy())
            cand_q = torch.from_numpy(_x01_from_b64_rgb(b64)).to(device)
            with torch.no_grad():
                pred = int(torch.argmax(model(cifar_normalize(cand_q)),dim=1).item())
            if pred == t:
                return cand_q.detach().cpu().numpy(), "ead"
        raise RuntimeError(f"EAD failed for sample {item.sample_id}")
    if item.required_method == "jacobian":
        adv = jsma_targeted(model, x, target=t, theta=0.12, gamma=0.15, max_iter=250)
        b64 = _to_b64_rgb_x01(adv.detach().cpu().numpy())
        cand_q = torch.from_numpy(_x01_from_b64_rgb(b64)).to(device)
        with torch.no_grad():
            pred = int(torch.argmax(model(cifar_normalize(cand_q)),dim=1).item())
        if pred != t:
            raise RuntimeError(f"JSMA failed for sample {item.sample_id}")
        return cand_q.detach().cpu().numpy(), "jacobian"
    # either
    print(f"[Sample {item.sample_id}] Trying JSMA first...")
    try:
        adv = jsma_targeted(model, x, target=t, theta=0.12, gamma=0.15, max_iter=250)
        b64 = _to_b64_rgb_x01(adv.detach().cpu().numpy())
        cand_q = torch.from_numpy(_x01_from_b64_rgb(b64)).to(device)
        with torch.no_grad():
            pred = int(torch.argmax(model(cifar_normalize(cand_q)),dim=1).item())
        if pred == t:
            print("  JSMA succeeded!")
            return cand_q.detach().cpu().numpy(), "jacobian"
        print("  JSMA failed, trying EAD...")
    except Exception as e:
        print(f"  JSMA error: {e}, trying EAD...")
    for params in [{"c":0.01,"beta":0.01,"lr":0.01,"max_iter":1000},{"c":0.005,"beta":0.02,"lr":0.01,"max_iter":1200}]:
        cand = ead_targeted(model, x, target=t, **params)
        b64 = _to_b64_rgb_x01(cand.detach().cpu().numpy())
        cand_q = torch.from_numpy(_x01_from_b64_rgb(b64)).to(device)
        with torch.no_grad():
            pred = int(torch.argmax(model(cifar_normalize(cand_q)),dim=1).item())
        if pred == t:
            print("  EAD succeeded!")
            return cand_q.detach().cpu().numpy(), "ead"
    raise RuntimeError(f"Both failed for sample {item.sample_id}")

def submit(host, bundle, advs, methods):
    items = [{"sample_id":it.sample_id,"method":methods[it.sample_id],"image_b64":_to_b64_rgb_x01(advs[it.sample_id])} for it in bundle]
    return _http_post_json(f"{host}/submit_images", {"items":items})

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="http://127.0.0.1:8000")
    parser.add_argument("--weights", default="cifar10_model.pth")
    args = parser.parse_args()
    set_seed()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    if device.type != "cuda":
        print("Warning: CUDA not available, running on CPU.")
    items = fetch_challenge(args.host)
    model = load_model(args.weights, device)
    advs = {}; methods = {}
    for it in items:
        adv_img, method_used = craft_adv(model, device, it)
        advs[it.sample_id] = adv_img
        methods[it.sample_id] = method_used
    resp = submit(args.host, items, advs, methods)
    print(json.dumps(resp, indent=2))
    if not resp.get("ok", False):
        raise SystemExit(2)
    print("Flag:", resp.get("flag"))

if __name__ == "__main__":
    main()

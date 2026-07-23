# DeepFool Challenge

Craft a targeted adversarial MNIST image using DeepFool to hit a specific target class
within an L2 threshold.

## Attack

Targeted DeepFool iteratively steps toward the target class decision boundary.

```python
def deepfool_targeted(model, x01, target, overshoot=0.08, max_iter=100):
    x01_t = torch.from_numpy(x01).float()
    r_tot = torch.zeros_like(x01_t)
    for _ in range(max_iter):
        x = torch.clamp(x01_t + (1+overshoot)*r_tot, 0, 1).detach().requires_grad_(True)
        logits = model(mnist_normalize(x))
        pred = logits.argmax(1).item()
        if pred == target:
            break
        # compute gradient difference between target and current class
        # step in minimal direction to cross boundary
    return torch.clamp(x01_t + (1+overshoot)*r_tot, 0, 1).detach().cpu().numpy()
```

Result: L2 0.718, threshold 0.75, clean digit 4 misclassified as digit 6

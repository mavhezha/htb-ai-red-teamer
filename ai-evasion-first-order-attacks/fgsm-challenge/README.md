# FGSM Challenge

Craft an adversarial MNIST image that causes misclassification within an L-inf epsilon budget.

## Attack

Single-step untargeted FGSM in [0,1] pixel space.

```python
def fgsm_untargeted(model, x01, y, epsilon):
    x = torch.from_numpy(x01).float().requires_grad_(True)
    loss = nn.NLLLoss()(model(mnist_normalize(x)), torch.tensor([y]))
    model.zero_grad()
    loss.backward()
    x_adv = torch.clamp(x + epsilon * x.grad.detach().sign(), 0.0, 1.0)
    return x_adv.detach().cpu().numpy()
```

## Key Details

- Model weights downloaded from /weights endpoint
- Safety margins tested to account for PNG quantization artifacts
- Clean digit 1 misclassified as digit 8

Result: L-inf 0.246, pred=8, clean_pred=1

# Skills Assessment 1: I-FGSM on CIFAR-10

Targeted iterative FGSM attack on a CIFAR-10 image classifier.
Goal: make a dog image classified as a cat within L-inf epsilon=0.031373.

## Attack

```python
def ifgsm_targeted(model, image, target_class, epsilon, mean, std, num_iterations=50, device="cpu"):
    alpha = epsilon / num_iterations
    mean_t = torch.tensor(mean, device=device).view(3,1,1)
    std_t = torch.tensor(std, device=device).view(3,1,1)
    x_adv = image.clone().to(device)
    x_orig = image.clone().to(device)
    target = torch.tensor([target_class], device=device)
    for i in range(num_iterations):
        x_norm = (x_adv - mean_t) / std_t
        x_norm.requires_grad = True
        loss = F.cross_entropy(model(x_norm.unsqueeze(0)), target)
        model.zero_grad()
        loss.backward()
        grad_pixel = x_norm.grad / std_t
        # Targeted: subtract gradient (minimize loss toward target)
        x_adv = x_orig + torch.clamp(x_adv - alpha * grad_pixel.sign() - x_orig, -epsilon, epsilon)
        x_adv = torch.clamp(x_adv, 0.0, 1.0).detach()
```

Result: Dog misclassified as cat at iteration 40/50

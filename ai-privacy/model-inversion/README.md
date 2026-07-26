# Model Inversion Attack

Reconstruct representative images of training classes by optimizing
an input image to maximize the model's confidence for a target class.

## Attack

```python
def invert_class(model, target_class, num_steps=5000, lr=0.05):
    x = torch.randn(1, 1, 28, 28, requires_grad=True)
    optimizer = optim.Adam([x], lr=lr)
    for step in range(num_steps):
        x_sig = torch.sigmoid(x)
        x_norm = (x_sig - MNIST_MEAN) / MNIST_STD
        logits = model(x_norm)
        ce_loss = F.nll_loss(logits, target)
        tv_loss = total_variation(x_sig)  # smoothness
        l2_loss = torch.sum(x_sig ** 2)   # magnitude
        loss = ce_loss + 1e-3*tv_loss + 1e-4*l2_loss
        loss.backward()
        optimizer.step()
    return torch.sigmoid(x)
```

Uses sigmoid parameterization to keep pixels in [0,1].
TV regularization promotes smooth, digit-like images.

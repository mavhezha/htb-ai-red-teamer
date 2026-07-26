# Skills Assessment: MIA Defense on Fashion-MNIST

Train a DP-SGD defended model that reduces baseline MIA advantage by 40%
while maintaining 70% test accuracy.

Baseline MIA advantage: 7.97%
Required: reduce to < 4.78%, maintain accuracy >= 70%

## Solution

DP-SGD with noise_multiplier=0.6 and max_grad_norm=1.2:

```python
model, optimizer, train_loader = privacy_engine.make_private(
    module=model,
    optimizer=optimizer,
    data_loader=train_loader,
    noise_multiplier=0.6,
    max_grad_norm=1.2,
)
```

## Result

MIA advantage: 0.82% (89.66% improvement)
Test accuracy: 76.1%
Score: 84.3/100

## Mac Notes

KMP_DUPLICATE_LIB_OK=TRUE python3 skills_assessment.py

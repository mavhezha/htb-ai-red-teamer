# DP-SGD Challenge (SVHN)

Train a differentially private model on SVHN that achieves:
- Test accuracy >= 55%
- MIA advantage <= 5%
- Privacy budget: epsilon <= 6.0

## Key Configuration

```python
TARGET_EPSILON = 6.0
DELTA = 1e-5
MAX_GRAD_NORM = 1.0
NOISE_MULTIPLIER = auto (from make_private_with_epsilon)
BATCH_SIZE = 256
EPOCHS = 20
```

## Result

Test accuracy: 78.51%, MIA advantage: 1.98%, epsilon: 5.99

## Mac Notes

KMP_DUPLICATE_LIB_OK=TRUE python3 dpsgd.py

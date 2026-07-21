# Label Flipping Attack

Randomly flip a percentage of training labels to corrupt learned decision boundaries.

## Task

Poison 60% of the dataset by flipping labels. Target: model accuracy near zero.

## Implementation

```python
def flip_labels(y, poison_percentage, seed):
    np.random.seed(seed)
    y_poisoned = y.copy()
    n_samples = len(y)
    n_to_flip = int(n_samples * poison_percentage)
    flipped_idx = np.random.choice(n_samples, size=n_to_flip, replace=False)
    y_poisoned[flipped_idx] = 1 - y_poisoned[flipped_idx]
    return y_poisoned, flipped_idx
```

Parameters: poison_rate=0.60, random_seed=1337

Result: Server accuracy 0.67% confirming successful poisoning.

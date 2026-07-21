# Targeted Label Attack

Flip labels of a specific class to make the model fail on that class while appearing healthy overall.

## Task

Flip 70% of Class 0 labels to Class 1. Target: Class 0 accuracy below threshold.

## Implementation

```python
def targeted_class_label_flip(y_train, target_class, new_label, poison_fraction, seed):
    np.random.seed(seed)
    y_train_poisoned = y_train.copy()
    target_indices = np.where(y_train_poisoned == target_class)[0]
    n_to_flip = int(poison_fraction * len(target_indices))
    flipped_indices = np.random.choice(target_indices, size=n_to_flip, replace=False)
    y_train_poisoned[flipped_indices] = new_label
    return y_train_poisoned, flipped_indices
```

Parameters: TARGET_CLASS_TO_POISON=0, NEW_LABEL=1, POISON_FRACTION=0.70

Result: Class 0 accuracy 4.58%, overall accuracy 51.33%.
The model looks functional in aggregate but is completely blind to Class 0.

# Skills Assessment: Class Ambiguity via Label Flipping

## Objective

Create ambiguity for Class 1 by flipping its labels to both Class 0 and Class 2,
causing the model to misclassify Class 1 samples while maintaining performance on Class 3.

## Attack Strategy

Flip 25% of Class 1 labels to Class 0 and 25% to Class 2.
Total: 50% of Class 1 samples poisoned.

## Implementation

```python
class1_indices = np.where(y_train_poisoned == 1)[0]
np.random.shuffle(class1_indices)

percent_to_flip_to_0 = 0.25
percent_to_flip_to_2 = 0.25

num_to_flip_to_0 = int(len(class1_indices) * percent_to_flip_to_0)
num_to_flip_to_2 = int(len(class1_indices) * percent_to_flip_to_2)

indices_to_make_0 = class1_indices[:num_to_flip_to_0]
indices_to_make_2 = class1_indices[num_to_flip_to_0:num_to_flip_to_0 + num_to_flip_to_2]

y_train_poisoned[indices_to_make_0] = 0
y_train_poisoned[indices_to_make_2] = 2
```

## Result

- Class 1 misclassified as Class 0: 38.4%
- Class 1 misclassified as Class 2: 52.8%
- Class 3 recall: 99.2%
- Overall accuracy: 75%

Attack criteria met: ambiguity thresholds exceeded for both directions.

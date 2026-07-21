# Clean Label Attack

Perturb training features without changing labels to cause misclassification of a specific target.

## Task

Misclassify Class 2 Index 334 as Class 1 without modifying any labels.

## Key Parameters

- EPSILON_CROSS = 0.25 (perturbation magnitude, critical value)
- target_idx = 334
- target_class = 2
- perturb_class = 1

## How It Works

1. Train a temporary baseline model to find the decision boundary between target and perturb classes
2. Identify neighbors of the perturb class closest to the target point
3. Calculate a perturbation vector perpendicular to the decision boundary
4. Apply perturbation to neighbor features, pushing them across the boundary
5. Labels remain unchanged so the poisoning is clean

Result: Overall accuracy 98.15%, target point misclassified as Class 1.

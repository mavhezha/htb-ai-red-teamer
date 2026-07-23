# Skills Assessment 2: DeepFool on CIFAR-10

Minimal L2 perturbation attack on a CIFAR-10 image classifier.
Goal: cause misclassification within L2 threshold of 3.5.

## Attack

DeepFool linearizes the classifier at each step and finds the closest decision boundary.

Key steps per iteration:
1. Compute gradients for each class k vs current class
2. Compute distance to each boundary: |f_k - f_cur| / ||w_k - w_cur||
3. Step in direction of closest boundary with overshoot
4. Convert gradient from normalized space to pixel space via chain rule

Result: Horse misclassified as truck in 3 iterations, L2=0.964, threshold=3.5

DeepFool finds significantly smaller perturbations than FGSM because it minimizes
the perturbation norm rather than using the full epsilon budget.

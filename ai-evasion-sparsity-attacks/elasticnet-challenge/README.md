# ElasticNet Challenge (EAD)

Craft an adversarial MNIST image using ElasticNet Attack with elastic-net regularization.

## Attack

EAD uses FISTA (Fast Iterative Shrinkage-Thresholding Algorithm) with binary search
over the regularization constant c.

Key components:
1. Adversarial loss: C&W margin formulation (max other class - target class + confidence)
2. L2 penalty: keeps perturbation magnitude small
3. L1 penalty (via soft-thresholding): promotes sparsity
4. Binary search: finds minimal c that achieves misclassification

## Result

Clean digit 9 misclassified as digit 8.
L1=10.74, L2=1.298, elastic=1.405, beta=0.01

# AI Evasion Sparsity Attacks

Sparsity attacks craft adversarial examples that modify as few features as possible
while still causing misclassification. Unlike L-inf or L2 attacks that bound the
magnitude of perturbation, sparsity attacks bound the number of modified features (L0).

## Labs

| Lab | Attack | Constraint | Key Insight |
|-----|--------|-----------|-------------|
| ElasticNet Challenge | EAD (FISTA) | Elastic-net (L1+L2) | Binary search over regularization constant |
| JSMA Challenge | JSMA | L0 (pixel count) | Jacobian saliency maps select most influential pixels |
| Skills Assessment | EAD + JSMA on CIFAR-10 | L0 / Elastic-net | Combined attack on ResNet-18 |

## Key Concepts

### ElasticNet Attack (EAD)
Uses FISTA optimization with elastic-net regularization (L1 + L2).
Binary search over constant c balances adversarial loss vs perturbation size.
L1 penalty promotes sparsity. L2 penalty keeps perturbation smooth.

### JSMA (Jacobian-based Saliency Map Attack)
Computes the Jacobian of the output w.r.t. each input pixel.
Saliency score for each pixel: how much does modifying it increase target class
while decreasing all other classes?
Iteratively selects highest-scoring pixel pairs until misclassification.

### Key Difference from First Order Attacks
FGSM/DeepFool modify all pixels within a budget.
JSMA modifies only the most influential pixels.
EAD combines both approaches: sparse (L1) and smooth (L2).

## Setup

```bash
conda activate ai
python3 -m pip install Pillow requests torch torchvision
```

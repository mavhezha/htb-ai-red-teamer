# AI Evasion First Order Attacks

First order attacks use gradient information to craft adversarial examples that
cause misclassification while staying within a bounded perturbation constraint.

## Labs

| Lab | Attack | Constraint | Key Insight |
|-----|--------|-----------|-------------|
| FGSM Challenge | Fast Gradient Sign Method | L-inf | Single step in gradient sign direction |
| DeepFool Challenge | DeepFool (targeted) | L2 | Iterative minimal boundary crossing |
| Skills Assessment 1 | I-FGSM (targeted) | L-inf | Iterative FGSM on CIFAR-10 |
| Skills Assessment 2 | DeepFool | L2 | Minimal perturbation on CIFAR-10 |

## Key Concepts

### FGSM
Single step attack. Compute gradient of loss w.r.t. input, take step in sign direction.
Fast but suboptimal. Budget is fully consumed in one step.

### I-FGSM
Iterative version of FGSM. Smaller steps, more iterations, better attack success rate.
For targeted attacks: minimize loss toward target class (negative gradient direction).

### DeepFool
Finds the minimal L2 perturbation by linearizing the classifier at each step,
computing the closest decision boundary, and stepping minimally across it.
Much more efficient than FGSM for finding small perturbations.

## Setup

```bash
conda activate ai
python3 -m pip install Pillow requests torch torchvision
```

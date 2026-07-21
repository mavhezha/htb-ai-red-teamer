# AI Data Attacks

AI Data Attacks target the training pipeline rather than the model itself.
By poisoning the data a model learns from, attackers corrupt model behavior
in ways that survive deployment and are difficult to detect.

## Labs

| Lab | Attack Type | Technique |
|-----|-------------|-----------|
| Label Flipping | Data Poisoning | Flip 60% of training labels randomly |
| Targeted Label Attack | Data Poisoning | Flip 70% of Class 0 labels to Class 1 |
| Clean Label Attack | Feature Poisoning | Perturb neighbor features to misclassify target |
| Trojan Attack | Backdoor | Embed trigger in MNIST images to force misclassification |
| Model Steganography | Supply Chain | Hide reverse shell payload in model weights via LSB encoding |
| Skills Assessment | Data Poisoning | Create class ambiguity via targeted multi-class label flipping |

## Key Concepts

### Data Poisoning vs Evasion
- Evasion attacks manipulate inputs at inference time
- Data attacks manipulate the training pipeline before deployment
- Data attacks are persistent and survive model retraining on poisoned data

### Types of Data Attacks
1. **Label Flipping**: Change the labels of training samples
2. **Clean Label**: Modify features without changing labels (harder to detect)
3. **Backdoor/Trojan**: Embed a trigger that causes misclassification only when present
4. **Supply Chain**: Hide malicious payloads in model weight files

## Setup

Labs run locally using JupyterLab with the conda `ai` environment.

```bash
conda activate ai
python3 -m pip install numpy scikit-learn matplotlib torch torchvision
jupyter lab
```

Key fix for Mac M2: always use `python3 -m pip` not `pip3` to install into the conda environment.

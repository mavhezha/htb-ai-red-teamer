# AI Evasion Foundations

AI evasion attacks manipulate inputs at inference time to cause misclassification
without modifying the model itself. Unlike data attacks which corrupt training,
evasion attacks work against deployed models.

## Labs

| Lab | Attack Type | Technique |
|-----|-------------|-----------|
| GoodWords Challenge | Text Evasion | Greedy word injection to flip spam classifier |
| Skills Assessment | White-box + Black-box | Feature log probability analysis + API-based word impact estimation |

## Key Concepts

### GoodWords Attack
Add words that shift the classifier's decision boundary without changing the
semantic meaning of the original message. The goal is to find words with the
highest impact on reducing spam probability.

### White-box vs Black-box

**White-box**: Full model access available. Use feature log probabilities directly
from the Naive Bayes classifier to rank words by their discriminative power for
the target class.

**Black-box**: No model access. Query the API with individual word additions and
measure the change in classification probability. Use greedy selection to build
the optimal word sequence.

## Setup

```bash
conda activate ai
python3 -m pip install scikit-learn numpy requests
```

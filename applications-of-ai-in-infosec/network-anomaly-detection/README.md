# Network Anomaly Detection

## Objective

Build and train a network intrusion detection model using the NSL-KDD dataset and submit
it to a live evaluation API.

## Approach

The model uses a Random Forest classifier for multi-class classification across five
traffic categories. Categorical features were one-hot encoded and combined with numeric
network flow statistics.

## Attack Categories

| Label | Category |
|-------|----------|
| 0 | Normal |
| 1 | DoS |
| 2 | Probe |
| 3 | Privilege Escalation |
| 4 | Access |

## Preprocessing Steps

1. Load NSL-KDD dataset with 43 columns
2. Map attack types to numeric categories
3. One-hot encode protocol_type and service columns
4. Join encoded features with numeric network statistics
5. Split into 80% train, 20% test with random_state=1337

## Results

- Validation accuracy: 99.5%
- Test accuracy: 100%

## Files

- `training_model.py` - Full training and evaluation script

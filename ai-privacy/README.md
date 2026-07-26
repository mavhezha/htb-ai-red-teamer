# AI Privacy

AI Privacy covers techniques for training models that protect sensitive information
about the data they were trained on, and attacks that attempt to extract that information.

## Labs

| Lab | Technique | Goal |
|-----|-----------|------|
| DP-SGD Challenge | Differential Privacy | Train SVHN model with epsilon<=6, accuracy>=55%, MIA advantage<=5% |
| PATE Challenge | Private Aggregation of Teachers | Train EMNIST Letters student model, accuracy>=80%, MIA advantage<=3% |
| Model Inversion | Attack | Reconstruct training data from model gradients |
| Skills Assessment | DP-SGD Defense | Reduce Fashion-MNIST MIA advantage by 40% while maintaining 70% accuracy |

## Key Concepts

### Differential Privacy
Adds calibrated noise to gradients during training. Guarantees that the model's
output changes by at most a bounded amount whether or not any single training
sample is included.

Key parameters:
- epsilon: privacy budget (lower = more private)
- delta: failure probability
- max_grad_norm: gradient clipping threshold
- noise_multiplier: controls noise scale

### PATE (Private Aggregation of Teachers Ensembles)
Train an ensemble of teacher models on disjoint private data.
Use noisy aggregated teacher votes to label public data.
Train a student model on the noisily-labeled public data.

Key parameters:
- num_teachers: more teachers = more privacy amplification
- noise_scale: Laplace noise added to vote counts
- confident_threshold: minimum votes needed to label a sample

### Membership Inference Attack (MIA)
Attacker tries to determine if a specific sample was in the training set.
Metric: MIA advantage = attack accuracy - 0.5 (0 = random, 0.5 = perfect)
Defended models should have MIA advantage close to 0.

## Mac M2 Notes

- Set KMP_DUPLICATE_LIB_OK=TRUE to avoid OpenMP conflicts with opacus
- Always use python3 -m pip not pip3 for conda environment

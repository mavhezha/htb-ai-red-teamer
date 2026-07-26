# PATE Challenge (EMNIST Letters)

Train a PATE student model on EMNIST Letters that achieves:
- Test accuracy >= 80%
- MIA advantage <= 3%

## Key Configuration

```python
NUM_TEACHERS = 25
NOISE_SCALE = 1.0
CONFIDENT_THRESHOLD = 15  # 60% consensus out of 25 teachers
STUDENT_EPOCHS = 120
```

## Architecture

Teachers: CNN (32->64 conv, 256 fc)
Student: MLP with layers.0 (784->256), layers.1 (256->128), output (128->26)

Note: Server validates exact parameter names. Student must use nn.ModuleList
named "layers" with indices 0 and 1, plus "output" layer.

## Key Steps

1. Load EMNIST Letters (labels 1-26, convert to 0-25)
2. Split: 80% private (teachers), 20% public (student labeling)
3. Normalize with StandardScaler
4. Train 25 teacher CNNs on disjoint private data
5. Aggregate votes on public data with Laplace noise
6. Filter to confident samples (threshold=15/25)
7. Train student MLP on noisily-labeled public data

## Result

Accuracy: 80.69%, MIA advantage: 0.68%

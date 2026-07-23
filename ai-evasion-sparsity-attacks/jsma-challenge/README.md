# JSMA Challenge

Craft a targeted adversarial MNIST image modifying as few pixels as possible.

## Attack

JSMA uses the Jacobian of the classifier output to identify which pixels,
when modified, will most effectively push the prediction toward the target class.

Key steps per iteration:
1. Compute Jacobian: how does each pixel affect each output class?
2. Compute saliency: which pixels increase target class AND decrease all others?
3. Evaluate pairwise saliency for pixel pairs
4. Modify the highest-scoring pair

Note: This challenge uses LeNet-5 architecture (Tanh activations, AvgPool)
not the SimpleClassifier CNN used in FGSM/DeepFool labs.

## Result

Digit 1 misclassified as digit 7.
Only 18 pixels modified out of 50-pixel budget.
Attack succeeded in 22 iterations.

# Trojan Attack (Backdoor)

Embed a hidden trigger in training data so the model behaves normally but misclassifies
any input containing the trigger.

## Task

Train a CNN on MNIST that misclassifies images of 7 as 1 when a white trigger
appears in the bottom left corner.

## Trigger Configuration

- SOURCE_CLASS = 7 (images to backdoor)
- TARGET_CLASS = 1 (class to predict when trigger is present)
- TRIGGER_POS = bottom left corner
- TRIGGER_SIZE = 3x3 white pixels
- TRIGGER_VAL = 1.0 (max brightness)
- POISON_RATE = fraction of source class images poisoned

## Key Functions

add_trigger(image_tensor): Adds the white square trigger to the bottom left.
PoisonedMNISTTrain: Dataset that applies trigger to source class and relabels them.
TriggeredMNISTTest: Test set with trigger applied to all source class images.

## Result

Clean Accuracy: 99.11%, Attack Success Rate: 99.90%

## Mac M2 Setup Note

Use python3 -m pip to install packages into conda environment.
torch.load requires weights_only=False for compatibility.

# Skills Assessment: EAD + JSMA on CIFAR-10 ResNet

Combined EAD and JSMA attack on a ResNet-18 classifier trained on CIFAR-10.
Server assigns required method per sample: "ead", "jacobian", or "either".

## Architecture

ResNetCIFAR (ResNet-18 adapted for CIFAR-10, no initial downsampling):
- BasicBlock with skip connections
- 4 layer groups: 64, 128, 256, 512 channels
- AdaptiveAvgPool2d + FC layer

## Key Differences from MNIST Labs

- RGB images (3 channels) vs grayscale
- 32x32 spatial resolution vs 28x28
- CIFAR-10 normalization: mean=(0.4914,0.4822,0.4465), std=(0.247,0.2435,0.2616)
- JSMA operates on pixel-level (all RGB channels summed for saliency)

## Result

JSMA succeeded on sample 0, server inferred as EAD based on perturbation signature.
L2=2.267, L-inf=0.239, diversity=1.

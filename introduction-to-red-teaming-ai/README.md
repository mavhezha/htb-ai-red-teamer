# Introduction to Red Teaming AI

HTB Academy module covering offensive attack techniques against machine learning systems.
Six labs covering the full spectrum of ML attack vectors.

## Labs

| Lab | Attack Type | Technique |
|-----|-------------|-----------|
| Input Manipulation | Evasion | Appending ham-like text to spam messages |
| Data Poisoning | Poisoning | Corrupting training labels to degrade accuracy |
| Model Theft | Extraction | Downloading model via unauthenticated endpoint |
| Text Generation | Prompt Manipulation | Forcing LLM to produce target phrase |
| Image Caption | Input Manipulation | Uploading image to trick vision model |
| Skills Assessment | Backdoor Injection | Poisoning training data with trigger phrase |

## Key Takeaway

AI models fail differently than traditional software. The attack surface is the training data,
the model file, and the inference pipeline, not just the application layer.

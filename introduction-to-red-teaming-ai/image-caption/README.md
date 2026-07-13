# Image Caption

## Objective

Upload a PNG image displaying the text "Hello World" so the model correctly identifies it.

## Approach

Found a clear PNG image of the text "Hello World" and uploaded it to the image caption
endpoint. The vision model performed OCR and text recognition on the image, correctly
identifying the text and returning the flag.

## Why This Matters

Vision models that perform OCR or text extraction can be manipulated by carefully crafted
images. In this case the task was benign, but the same technique applies offensively:
attackers can craft images containing adversarial text that causes models to misread
content, bypass filters, or produce unintended outputs.

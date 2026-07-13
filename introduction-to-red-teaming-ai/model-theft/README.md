# Model Theft

## Objective

Steal the trained model by exploiting a flaw in the web application.

## Approach

Inspected the page source of the target web application by right-clicking and selecting
View Page Source. Found a commented-out endpoint on line 19:

```html
<!-- /model -->
```

Downloaded the model file directly using curl and computed its MD5 hash.

## Key Commands

```bash
curl -o model http://TARGET_IP:PORT/model
md5sum model
```

## Result

Successfully downloaded the trained model file. The MD5 hash of the file was the flag.

## Why This Works

The model endpoint had no authentication, rate limiting, or access controls. A commented
endpoint in HTML source is still accessible. Developers often leave debug or admin endpoints
active in production without realizing they expose sensitive assets.

## Security Implications

A stolen model can be used to run offline inference, craft adversarial inputs without
sending requests to the target, reverse engineer decision boundaries, and clone the model
for competitive or malicious purposes.

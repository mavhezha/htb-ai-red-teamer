# Input Manipulation

## Objective

Manipulate a fixed spam message to trick the classifier into classifying it as ham
by appending text to the message.

## Target Message

```
Congratulations! You've won a $1000 Walmart gift card. Go to https://bit.ly/3YCN7PF to claim now.
```

## Approach

The spam classifier uses a Naive Bayes model that makes decisions based on word frequency
across the entire message. By appending a large block of legitimate-looking text, the spam
keywords become a small fraction of the total word count, tipping the classifier toward ham.

This is called a **dilution attack** or **stuffing attack**. The model has no concept of
message structure so it cannot distinguish between the malicious prefix and the appended text.

## Payload

Appended a Lorem Ipsum paragraph of approximately 200 words directly after the spam message.
The classifier then saw a low density of spam keywords relative to total word count and
classified the combined message as ham.

## Why This Works

Naive Bayes computes the probability of spam based on the presence and frequency of words.
Adding hundreds of neutral words mathematically reduces the spam probability even though
the malicious content is still present.

## Result

Classifier output: Not Spam

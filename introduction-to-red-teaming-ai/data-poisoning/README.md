# Data Poisoning

## Objective

Manipulate the training dataset to reduce the trained classifier accuracy below 70%.

## Approach

Downloaded the training dataset from the lab interface. Extracted the first 100 rows
into a separate CSV file. Used find and replace in a text editor to flip most ham labels
to spam, leaving only a small number of legitimate ham entries.

The poisoned dataset overwhelmingly labeled messages as spam regardless of content,
causing the model to learn incorrect decision boundaries.

## Key Command

```bash
head -n 101 training_data.csv > poison-student.csv
```

Then edited poison-student.csv to change ham labels to spam, keeping only 2 to 3
legitimate ham entries so spam heavily outweighed ham.

## Result

Model accuracy dropped to 11.2%, well below the 70% threshold.

## Why This Works

Supervised learning models learn entirely from labeled training data. If the labels
are wrong, the model learns wrong patterns. This is the fundamental vulnerability
of any ML system that trains on data it does not fully control or verify.

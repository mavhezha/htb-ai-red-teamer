# Spam Detection

## Objective

Build and train a spam detection model using the SMS Spam Collection dataset and submit
it to a live evaluation API.

## Approach

The model uses a Naive Bayes classifier inside a scikit-learn Pipeline with CountVectorizer
for feature extraction. GridSearchCV was used to tune the alpha hyperparameter across eight
values, with cross-validation selecting 0.25 as optimal.

## Preprocessing Steps

1. Convert text to lowercase
2. Remove punctuation and special characters
3. Tokenize using NLTK word tokenizer
4. Remove English stop words
5. Apply Porter Stemmer to reduce words to their root form

## Model Pipeline

```
Raw SMS Text
      |
CountVectorizer (ngram_range=(1,2), min_df=1, max_df=0.9)
      |
MultinomialNB (alpha=0.25)
      |
Spam / Not Spam
```

## Results

- Best alpha: 0.25
- Evaluation accuracy: 91%

## Files

- `training_model.py` - Full training and evaluation script

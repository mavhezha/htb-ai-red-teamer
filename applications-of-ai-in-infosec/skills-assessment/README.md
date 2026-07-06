# Skills Assessment: Sentiment Analysis

## Objective

Build a sentiment classifier for movie reviews using the IMDB dataset and submit it
to a live evaluation API.

## Approach

The model uses a Naive Bayes classifier inside a scikit-learn Pipeline with
CountVectorizer for feature extraction. The key challenge was handling HTML tags
present in the raw review text such as br tags used for line breaks.

## Preprocessing Steps

1. Convert text to lowercase
2. Strip HTML tags using regex
3. Remove punctuation and non-word characters
4. Remove extra whitespace
5. Vectorize using unigrams and bigrams

## Model Pipeline

```
Raw Review Text
      |
Clean HTML and punctuation
      |
CountVectorizer (ngram_range=(1,2), stop_words=english)
      |
MultinomialNB
      |
Good / Bad Review
```

## Results

- Evaluation accuracy: 100%

## Files

- `assessment.py` - Full training, evaluation, and upload script

import os
import re
import nltk
import pandas as pd
import numpy as np
import requests
import zipfile
import io
import joblib
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline


def download_dataset(url, extract_to):
    response = requests.get(url)
    if response.status_code == 200:
        print("Download successful")
        with zipfile.ZipFile(io.BytesIO(response.content)) as z:
            z.extractall(extract_to)
            print("Extraction successful")
    else:
        print("Failed to download the dataset")


def preprocess_message(message, stop_words, stemmer):
    message = message.lower()
    message = re.sub(r"[^a-z\s$!]", "", message)
    tokens = word_tokenize(message)
    tokens = [word for word in tokens if word not in stop_words]
    tokens = [stemmer.stem(word) for word in tokens]
    return " ".join(tokens)


def load_and_preprocess_data(file_path):
    df = pd.read_csv(file_path, sep="\t", header=None, names=["label", "message"])
    df.drop_duplicates(inplace=True)

    nltk.download("punkt_tab")
    nltk.download("stopwords")
    stop_words = set(stopwords.words("english"))
    stemmer = PorterStemmer()

    df["message"] = df["message"].apply(lambda x: preprocess_message(x, stop_words, stemmer))
    df["label"] = df["label"].apply(lambda x: 1 if x == "spam" else 0)

    return df


def train_model(df):
    X = df["message"]
    y = df["label"]

    vectorizer = CountVectorizer(min_df=1, max_df=0.9, ngram_range=(1, 2))
    pipeline = Pipeline([
        ("vectorizer", vectorizer),
        ("classifier", MultinomialNB())
    ])

    param_grid = {"classifier__alpha": [0.01, 0.1, 0.15, 0.2, 0.25, 0.5, 0.75, 1.0]}
    grid_search = GridSearchCV(pipeline, param_grid, cv=5, scoring="f1")
    grid_search.fit(X, y)

    best_model = grid_search.best_estimator_
    print("Best model parameters:", grid_search.best_params_)

    return best_model


def save_model(model, filename):
    joblib.dump(model, filename)
    print(f"Model saved to {filename}")


def load_model(filename):
    return joblib.load(filename)


def predict_messages(model, messages):
    predictions = model.predict(messages)
    probabilities = model.predict_proba(messages)

    for i, msg in enumerate(messages):
        prediction = "Spam" if predictions[i] == 1 else "Not-Spam"
        spam_probability = probabilities[i][1]
        ham_probability = probabilities[i][0]

        print(f"Message: {msg}")
        print(f"Prediction: {prediction}")
        print(f"Spam Probability: {spam_probability:.2f}")
        print(f"Not-Spam Probability: {ham_probability:.2f}")
        print("-" * 50)


if __name__ == "__main__":
    dataset_url = "https://archive.ics.uci.edu/static/public/228/sms+spam+collection.zip"
    extract_path = "sms_spam_collection"

    download_dataset(dataset_url, extract_path)
    dataset_path = os.path.join(extract_path, "SMSSpamCollection")
    df = load_and_preprocess_data(dataset_path)

    model = train_model(df)
    save_model(model, "spam_detection_model.joblib")

    new_messages = [
        "Congratulations! You've won a $1000 Walmart gift card. Go to http://bit.ly/1234 to claim now.",
        "Hey, are we still meeting up for lunch today?",
        "FREE entry in a weekly competition to win an iPad. Just text WIN to 80085 now!",
    ]

    loaded_model = load_model("spam_detection_model.joblib")
    predict_messages(loaded_model, new_messages)

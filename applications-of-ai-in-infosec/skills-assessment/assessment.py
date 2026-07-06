import requests
import zipfile
import io
import pandas as pd
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import joblib
import sys
import json


def download():
    url = "https://academy.hackthebox.com/storage/modules/292/skills_assessment_data.zip"
    response = requests.get(url)
    if response.status_code == 200:
        print("Download successful")
        with zipfile.ZipFile(io.BytesIO(response.content)) as z:
            z.extractall("skills_assessment_data")
            print("Extraction successful")
    else:
        print("Failed to download the dataset")


def dataset():
    df = pd.read_json("skills_assessment_data/train.json", orient="records")
    df.info()
    df = df.drop_duplicates()
    return df


def clean_text(text):
    text = re.sub(r"<.*?>", " ", text)
    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def preprocessing(df):
    df["text"] = df["text"].apply(lambda x: x.lower())
    df["text"] = df["text"].apply(clean_text)
    return df


def train_model(df):
    X_train, X_test, y_train, y_test = train_test_split(
        df["text"], df["label"], test_size=0.3, random_state=42
    )

    pipeline = Pipeline([
        ("vectorizer", CountVectorizer(
            lowercase=True,
            stop_words="english",
            token_pattern=r"\b\w+\b",
            ngram_range=(1, 2)
        )),
        ("classifier", MultinomialNB())
    ])

    print("Training model...")
    pipeline.fit(X_train, y_train)
    print("Training complete!")

    model_filename = "assessment.joblib"
    joblib.dump(pipeline, model_filename)
    print(f"Model saved to {model_filename}")

    return pipeline


def evaluate_model(model, new_texts):
    print("\nEvaluating new texts:")
    predictions = model.predict(new_texts)
    probabilities = model.predict_proba(new_texts)

    for text, pred, prob in zip(new_texts, predictions, probabilities):
        pred_label = "Good" if pred == 1 else "Bad"
        print(f"Text: {text[:60]}...")
        print(f"  -> Prediction: {pred_label} | Probabilities: {prob}")


def upload_model(pipeline):
    target = sys.argv[1]
    url = f'http://{target}:5000/api/upload'

    model_file_path = 'assessment.joblib'
    with open(model_file_path, "rb") as model_file:
        files = {"model": model_file}
        response = requests.post(url, files=files)

    print(json.dumps(response.json(), indent=4))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f'Usage: {sys.argv[0]} <target_ip>')
        sys.exit(1)

    target = sys.argv[1]

    download()
    df = dataset()
    df = preprocessing(df)

    model = train_model(df)

    new_texts = [
        "I went and saw this movie last night after being coaxed to by a few friends of mine.",
        "This was the worst movie I have ever seen in my life. Total waste of time.",
        "Bill Paxton has taken the true story of the 1913 US golf open and made a great film."
    ]

    evaluate_model(model, new_texts)
    upload_model(model)

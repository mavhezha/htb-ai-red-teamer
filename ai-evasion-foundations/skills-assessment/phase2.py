#!/usr/bin/env python3
import os, requests, numpy as np
from typing import List, Dict, Tuple

SEED = 1337
np.random.seed(SEED)
BASE_URL = os.environ.get("BASE_URL", "http://localhost:8080")

class BlackBoxAttacker:
    def __init__(self, base_url):
        self.base_url = base_url
        self.word_impacts = {}
        self.query_count = 0

    def predict(self, text):
        self.query_count += 1
        r = requests.post(f"{self.base_url}/predict", json={"text": text})
        r.raise_for_status()
        return r.json()

    def estimate_word_impacts(self, base_text, vocabulary):
        base_pred = self.predict(base_text)
        base_pos_prob = base_pred["positive_probability"]
        impacts = []
        for word in vocabulary:
            augmented = base_text + " " + word
            pred = self.predict(augmented)
            impact = pred["positive_probability"] - base_pos_prob
            impacts.append((word, impact))
        impacts.sort(key=lambda x: x[1], reverse=True)
        return impacts

    def attack_review(self, text, max_words):
        positive_vocabulary = [
            "excellent", "amazing", "wonderful", "fantastic", "brilliant",
            "outstanding", "superb", "magnificent", "perfect", "exceptional",
            "masterpiece", "genius", "beautiful", "stunning", "remarkable",
            "awesome", "incredible", "phenomenal", "spectacular", "marvelous",
            "great", "good", "love", "loved", "best", "favorite", "enjoyed",
            "recommend", "highly", "definitely", "must", "liked", "appreciate",
            "admire", "adore", "enjoy", "compelling", "engaging", "captivating",
            "mesmerizing", "powerful", "touching", "moving", "inspiring",
            "uplifting", "heartwarming", "clever", "witty", "funny", "hilarious",
            "entertaining"
        ]
        impacts = self.estimate_word_impacts(text, positive_vocabulary[:50])
        augmented = text
        for i, (word, impact) in enumerate(impacts, 1):
            if i > max_words:
                break
            augmented = augmented + " " + word
            pred = self.predict(augmented)
            if pred["label"] == "positive":
                return augmented, i
        if impacts:
            top_words = [w for w, _ in impacts[:10]]
            words_to_add = []
            while len(words_to_add) < max_words:
                words_to_add.extend(top_words)
            augmented = text + " " + " ".join(words_to_add[:max_words])
        return augmented, max_words

    def solve_blackbox(self):
        print("\n[*] Starting black-box phase...")
        r = requests.get(f"{self.base_url}/challenge/blackbox")
        r.raise_for_status()
        challenge = r.json()
        reviews = challenge["reviews"]
        max_words = challenge["max_added_words"]
        solutions = []
        for review in reviews:
            print(f"  Attacking review {review['id']}...", end=" ")
            augmented, words_used = self.attack_review(review["text"], max_words)
            solutions.append({"id": review["id"], "augmented_text": augmented})
            print(f"Done ({words_used} words, {self.query_count} queries total)")
        r = requests.post(f"{self.base_url}/submit/blackbox", json={"solutions": solutions})
        r.raise_for_status()
        result = r.json()
        if "results" in result:
            successes = sum(1 for r in result["results"] if r.get("success", False))
            print(f"[+] Black-box phase: {successes}/10 completed")
        return result

def main():
    bb_attacker = BlackBoxAttacker(BASE_URL)
    bb_result = bb_attacker.solve_blackbox()
    if bb_result.get("flag"):
        print("\n" + "=" * 60)
        print("[+] SUCCESS! All challenges completed!")
        print(f"[+] Flag: {bb_result['flag']}")
        print("=" * 60)
    else:
        print("[-] Failed to complete black-box phase")

if __name__ == "__main__":
    main()

# Skills Assessment: White-box and Black-box Evasion

Two-phase evasion challenge against a sentiment classifier.

## Phase 1: White-box

Download model via /model/download. Use Naive Bayes feature log probabilities
to rank words by association with target class. Result: 10/10 reviews flipped.

## Phase 2: Black-box

No model access. Query /predict with individual word additions to estimate impact.
Greedily add highest-impact words. Result: 10/10 reviews flipped, 714 API queries.

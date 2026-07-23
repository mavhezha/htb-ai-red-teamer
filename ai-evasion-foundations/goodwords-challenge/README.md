# GoodWords Challenge

Flip a spam classifier from spam to ham by appending up to 25 words.

## Approach

1. Fetch challenge parameters from /challenge
2. Test each candidate word to measure spam probability reduction
3. Rank words by impact
4. Greedily append highest-impact words until classifier flips

Result: 8 words added, final spam probability 10.77%.

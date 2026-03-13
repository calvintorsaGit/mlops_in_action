# Day 7: Week 1 Review and Mini Project

## Goal

Combine everything from Day 1-6 into one working project. By the end of today, you should have a GitHub repo where:

1. Model training is tracked with MLflow
2. The model is served via FastAPI
3. Everything is packaged in Docker
4. Tests run automatically via GitHub Actions

---

## Project Structure

```
taxi-fare-mlops/
├── .github/
│   └── workflows/
│       └── ml-pipeline.yml       # CI/CD pipeline
├── src/
│   ├── train.py                  # Train model + log to MLflow
│   ├── predict.py                # FastAPI prediction server
│   └── preprocess.py             # Data cleaning functions
├── tests/
│   ├── test_preprocess.py        # Unit tests
│   └── test_model.py             # Model quality tests
├── Dockerfile                    # Container setup
├── requirements.txt              # Dependencies
└── README.md                     # How to run the project
```

---

## Step-by-Step

### 1. Create `src/preprocess.py`

```python
import pandas as pd

def clean_data(df):
    df = df.dropna()
    df = df[df["trip_distance"] > 0]
    df = df[df["fare_amount"] > 0]
    df = df[df["passenger_count"] > 0]
    return df

def get_features_and_target(df):
    X = df[["trip_distance", "passenger_count"]]
    y = df["fare_amount"]
    return X, y
```

### 2. Create `src/train.py`

```python
import mlflow
import mlflow.sklearn
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from preprocess import clean_data, get_features_and_target

mlflow.set_experiment("taxi-fare-weekly")

# Generate or load data
np.random.seed(42)
data = pd.DataFrame({
    "trip_distance": np.random.uniform(1, 20, 1000),
    "passenger_count": np.random.randint(1, 6, 1000),
})
data["fare_amount"] = 2.5 + (data["trip_distance"] * 2.8) + np.random.normal(0, 2, 1000)

# Preprocess
data = clean_data(data)
X, y = get_features_and_target(data)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train and track
with mlflow.start_run(run_name="week1-baseline"):
    model = LinearRegression()
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    mae = mean_absolute_error(y_test, preds)
    rmse = np.sqrt(mean_squared_error(y_test, preds))
    r2 = r2_score(y_test, preds)

    mlflow.log_param("model_type", "LinearRegression")
    mlflow.log_metric("mae", mae)
    mlflow.log_metric("rmse", rmse)
    mlflow.log_metric("r2", r2)
    mlflow.sklearn.log_model(model, "model")

    # Also save locally for the API
    import joblib
    joblib.dump(model, "model.pkl")

    print(f"MAE: {mae:.4f} | RMSE: {rmse:.4f} | R2: {r2:.4f}")
```

### 3. Create `src/predict.py`

```python
from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np

app = FastAPI()
model = joblib.load("model.pkl")

class TripInput(BaseModel):
    trip_distance: float
    passenger_count: int

@app.post("/predict")
def predict(trip: TripInput):
    X = np.array([[trip.trip_distance, trip.passenger_count]])
    pred = model.predict(X)
    return {"fare_amount": round(float(pred[0]), 2)}

@app.get("/health")
def health():
    return {"status": "ok"}
```

### 4. Write tests, Dockerfile, CI/CD

Use what you built in Day 3-6. Refer to:
- [03-ci-cd.md](03-ci-cd.md) for tests and GitHub Actions
- [02-model-packaging.md](02-model-packaging.md) for Dockerfile

### 5. Run everything locally

```bash
# Train the model
python src/train.py

# Run tests
pytest tests/ -v

# Run the API
uvicorn src.predict:app --host 0.0.0.0 --port 8000

# Build and run in Docker
docker build -t taxi-fare-api .
docker run -p 8000:8000 taxi-fare-api
```

### 6. Push to GitHub

```bash
git init
git add .
git commit -m "Week 1: MLflow + FastAPI + Docker + CI/CD"
git remote add origin https://github.com/yourusername/taxi-fare-mlops.git
git push -u origin main
```

Check the Actions tab to see your CI pipeline run.

---

## Self-Check

Before moving to Week 2, make sure you can answer:

- [ ] What is experiment tracking and why does it matter?
- [ ] What are parameters, metrics, and artifacts in MLflow?
- [ ] What is the difference between a Docker image and a container?
- [ ] What does CI/CD stand for and what problem does it solve?
- [ ] What types of tests should you write for ML code?
- [ ] Can someone clone your repo, run it, and get predictions?

---

Next: [05-pipeline-orchestration.md](05-pipeline-orchestration.md)

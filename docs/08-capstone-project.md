# Day 14: Capstone Project

## Goal

Build a complete end-to-end MLOps project that connects everything from the past 2 weeks. This is your portfolio piece.

---

## What You're Building

A taxi fare prediction service with:

1. **Data versioning** — DVC tracks the dataset
2. **Experiment tracking** — MLflow logs every training run
3. **Automated pipeline** — Prefect orchestrates the workflow
4. **Model serving** — FastAPI exposes a prediction endpoint
5. **Containerization** — Docker packages everything
6. **CI/CD** — GitHub Actions automates testing and deployment
7. **Monitoring** — Evidently checks for data drift

---

## Project Structure

```
taxi-fare-mlops/
├── .github/
│   └── workflows/
│       └── ml-pipeline.yml
├── data/
│   ├── taxi_data.csv
│   └── taxi_data.csv.dvc
├── src/
│   ├── preprocess.py
│   ├── train.py
│   ├── predict.py
│   ├── pipeline.py
│   └── monitor.py
├── tests/
│   ├── test_preprocess.py
│   ├── test_model.py
│   └── test_api.py
├── Dockerfile
├── requirements.txt
├── dvc.yaml
└── README.md
```

---

## Step-by-Step

### 1. Set up the project

```bash
mkdir taxi-fare-mlops
cd taxi-fare-mlops
git init
dvc init
```

### 2. Version your data

```bash
dvc add data/taxi_data.csv
git add data/taxi_data.csv.dvc .gitignore
git commit -m "Track dataset with DVC"
```

### 3. Build the pipeline (src/pipeline.py)

```python
from prefect import flow, task
import mlflow
import mlflow.sklearn
import pandas as pd
import numpy as np
import joblib
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

@task(name="load-data", retries=2)
def load_data():
    data = pd.read_csv("data/taxi_data.csv")
    print(f"Loaded {len(data)} rows")
    return data

@task(name="preprocess")
def preprocess(data):
    data = data.dropna()
    data = data[data["trip_distance"] > 0]
    data = data[data["fare_amount"] > 0]
    return data

@task(name="train")
def train(data):
    X = data[["trip_distance", "passenger_count"]]
    y = data["fare_amount"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    mlflow.set_experiment("taxi-fare-capstone")
    with mlflow.start_run():
        model = LinearRegression()
        model.fit(X_train, y_train)
        preds = model.predict(X_test)

        mae = mean_absolute_error(y_test, preds)
        rmse = np.sqrt(mean_squared_error(y_test, preds))
        r2 = r2_score(y_test, preds)

        mlflow.log_metric("mae", mae)
        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("r2", r2)
        mlflow.sklearn.log_model(model, "model")

        print(f"MAE: {mae:.4f} | RMSE: {rmse:.4f} | R2: {r2:.4f}")

    joblib.dump(model, "model.pkl")
    return model

@task(name="monitor")
def check_drift(data):
    from evidently.report import Report
    from evidently.metric_preset import DataDriftPreset

    mid = len(data) // 2
    ref = data.iloc[:mid]
    cur = data.iloc[mid:]

    report = Report(metrics=[DataDriftPreset()])
    report.run(reference_data=ref, current_data=cur)

    result = report.as_dict()
    drift = result["metrics"][0]["result"]["dataset_drift"]
    print(f"Drift detected: {drift}")
    return drift

@flow(name="capstone-pipeline")
def run_pipeline():
    data = load_data()
    clean = preprocess(data)
    model = train(clean)
    drift = check_drift(clean)

    if drift:
        print("WARNING: Data drift detected. Review before deploying.")
    else:
        print("No drift. Safe to deploy.")

if __name__ == "__main__":
    run_pipeline()
```

### 4. Create the API (src/predict.py)

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

### 5. Dockerize, test, and push

Refer to:
- [02-model-packaging.md](02-model-packaging.md) for Docker setup
- [03-ci-cd.md](03-ci-cd.md) for tests and GitHub Actions

---

## Final Checklist

After completing the capstone, verify:

- [ ] Dataset is versioned with DVC
- [ ] Training runs are logged in MLflow
- [ ] Pipeline runs end-to-end with Prefect
- [ ] API returns predictions via FastAPI
- [ ] Everything runs inside Docker
- [ ] GitHub Actions runs tests on push
- [ ] Drift detection runs as part of the pipeline
- [ ] README explains how to set up and run the project
- [ ] Someone else can clone the repo and run it

---

## What's Next

You've covered the fundamentals. Here's where to go deeper:

| Topic | Resource |
|-------|----------|
| Feature stores | Feast (feast.dev) |
| Advanced orchestration | Apache Airflow |
| Model explainability | SHAP, LIME |
| ML platform | Kubeflow, MLRun |
| LLMOps | LangChain, vLLM, MLflow for LLMs |
| Certification | Google Cloud ML Engineer, AWS ML Specialty |

---

Previous: [07-cloud-deployment.md](07-cloud-deployment.md)

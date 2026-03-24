# Day 1-2: Experiment Tracking

## The Problem

You train a model, tweak some settings, train again. Repeat 30 times. Now you have no idea which run had the best results or what settings you used.

Without experiment tracking, you're guessing.

---

## The Solution

Experiment tracking means logging everything about every training run automatically — what settings you used, what results you got, and what model file was produced.

### What Gets Tracked

Every run records three things:

**Parameters** — the inputs you chose:
- model_type = "RandomForest"
- learning_rate = 0.01
- n_estimators = 100

**Metrics** — the results you measured:
- accuracy = 0.87
- rmse = 4.52
- training_time = 45s

**Artifacts** — the files you saved:
- model.pkl
- confusion_matrix.png

---

## Tool: MLflow

MLflow is the most popular open-source experiment tracking tool. It logs your runs and gives you a web dashboard to compare them.

### Install

```bash
pip install mlflow scikit-learn pandas
```

### How MLflow is organized

```
MLflow
├── Tracking        — log parameters, metrics, artifacts
├── Projects        — package code for reproducibility
├── Models          — standard format for saving models
└── Model Registry  — version and promote models (Staging -> Production)
```

---

## Hands-On: Track Your First Experiment

### Step 1: Basic tracking

```python
# experiment_basic.py
import mlflow
import mlflow.sklearn
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import pandas as pd
import numpy as np

# Set up MLflow
mlflow.set_tracking_uri("mlruns")
mlflow.set_experiment("taxi-fare-v1")

# Create sample data
np.random.seed(42)
data = pd.DataFrame({
    "trip_distance": np.random.uniform(1, 20, 1000),
    "passenger_count": np.random.randint(1, 6, 1000),
})
data["fare_amount"] = 2.5 + (data["trip_distance"] * 2.8) + np.random.normal(0, 2, 1000)

X = data[["trip_distance", "passenger_count"]]
y = data["fare_amount"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train and track
with mlflow.start_run(run_name="linear-baseline"):
    # Log parameters
    mlflow.log_param("model_type", "LinearRegression")
    mlflow.log_param("features", "trip_distance, passenger_count")
    mlflow.log_param("test_size", 0.2)

    # Train
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Evaluate
    predictions = model.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)
    rmse = np.sqrt(mean_squared_error(y_test, predictions))
    r2 = r2_score(y_test, predictions)

    # Log metrics
    mlflow.log_metric("mae", mae)
    mlflow.log_metric("rmse", rmse)
    mlflow.log_metric("r2", r2)

    # Save model
    mlflow.sklearn.log_model(model, "model")

    print(f"MAE:  {mae:.4f}")
    print(f"RMSE: {rmse:.4f}")
    print(f"R2:   {r2:.4f}")
```

### Step 2: Run it

```bash
python experiment_basic.py
```

### Step 3: View results in the dashboard

```bash
mlflow ui
```

Open http://localhost:5000. You'll see your experiment, your run, and all logged data.

---

## Comparing Multiple Runs

This is where tracking pays off. Train several models and compare them:

```python
# experiment_comparison.py
import mlflow
import mlflow.sklearn
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import pandas as pd
import numpy as np

mlflow.set_experiment("taxi-fare-v1")

# Prepare data
np.random.seed(42)
data = pd.DataFrame({
    "trip_distance": np.random.uniform(1, 20, 1000),
    "passenger_count": np.random.randint(1, 6, 1000),
})
data["fare_amount"] = 2.5 + (data["trip_distance"] * 2.8) + np.random.normal(0, 2, 1000)

X = data[["trip_distance", "passenger_count"]]
y = data["fare_amount"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Models to compare
models = {
    "LinearRegression": LinearRegression(),
    "Ridge": Ridge(alpha=1.0),
    "Lasso": Lasso(alpha=0.1),
    "RandomForest": RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42),
}

for name, model in models.items():
    with mlflow.start_run(run_name=name):
        mlflow.log_param("model_type", name)

        model.fit(X_train, y_train)
        preds = model.predict(X_test)

        mae = mean_absolute_error(y_test, preds)
        rmse = np.sqrt(mean_squared_error(y_test, preds))
        r2 = r2_score(y_test, preds)

        mlflow.log_metric("mae", mae)
        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("r2", r2)

        mlflow.sklearn.log_model(model, "model")

        print(f"{name:20s} | MAE: {mae:.4f} | RMSE: {rmse:.4f} | R2: {r2:.4f}")
```

Run it, then check the MLflow UI. You can select runs and compare them in a chart.

---

## Model Registry

Once you find the best model, you register it. This gives it a name, a version number, and a stage.

Stages:
- **None** — just registered, not used yet
- **Staging** — being tested
- **Production** — live and serving predictions
- **Archived** — old, no longer used

```python
# Register a model from a run
result = mlflow.register_model(
    model_uri="runs:/<RUN_ID>/model",
    name="taxi-fare-model"
)

# Promote to production
from mlflow.tracking import MlflowClient
client = MlflowClient()
client.transition_model_version_stage(
    name="taxi-fare-model",
    version=1,
    stage="Production"
)
```

Replace `<RUN_ID>` with the actual run ID from MLflow UI.

---

## Bonus: Data Version Control (DVC)

MLflow tracks code and models. DVC tracks data.

Datasets are too big for Git. DVC creates a small pointer file that Git tracks, while the actual data is stored elsewhere (local folder, S3, GCS).

```bash
pip install dvc
dvc init
dvc add data/taxi_data.csv

git add data/taxi_data.csv.dvc .gitignore
git commit -m "Track taxi data v1"
```

Now you can go back to any data version, just like going back to any code commit with Git.

---

## Key Takeaways

- Experiment tracking saves you from losing track of what worked
- Log parameters, metrics, and artifacts for every run
- MLflow UI lets you compare runs visually
- Model Registry manages model versions and stages
- DVC versions your datasets

---

## Practice

1. Train 3 different models, log them to MLflow, and compare in the UI
2. Try different hyperparameters for Ridge (vary alpha) and log each run
3. Register the best model and promote it to Production stage
4. (Bonus) Use DVC to version a dataset

---

Next: [02-model-packaging.md](02-model-packaging.md)

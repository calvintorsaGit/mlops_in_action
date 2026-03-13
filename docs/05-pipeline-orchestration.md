# Day 8-9: Pipeline Orchestration

## The Problem

Your ML workflow has multiple steps:

```
Get data → Clean data → Feature engineering → Train → Evaluate → Deploy
```

Right now you run these manually, one by one. If step 3 fails, you restart from the beginning. If you want to run this every day, you have to babysit it.

---

## The Solution

A pipeline orchestrator runs your steps in order, handles failures, retries, scheduling, and gives you a dashboard to see what's happening.

Think of it like an assembly line in a factory. Each station does one thing, and the whole line runs automatically.

---

## Tool Comparison

| Tool | Complexity | Best for |
|------|-----------|----------|
| **Prefect** | Low | Python-native, easy to start with |
| **Apache Airflow** | High | Enterprise, large-scale scheduling |
| **Kubeflow Pipelines** | High | Kubernetes-based ML workflows |
| **ZenML** | Medium | MLOps-specific pipelines |

We'll use **Prefect** because it's the simplest to learn and uses plain Python.

---

## Install Prefect

```bash
pip install prefect
```

---

## Core Concepts

| Concept | What it is |
|---------|-----------|
| **Task** | A single step in your pipeline (a Python function with `@task`) |
| **Flow** | The full pipeline that connects tasks together (a function with `@flow`) |
| **Run** | One execution of a flow |
| **Retry** | Automatically re-run a task if it fails |
| **Schedule** | Run a flow on a timer (daily, hourly, etc.) |

```
@flow
def my_pipeline():
    data = load_data()          # @task
    clean = preprocess(data)    # @task
    model = train(clean)        # @task
    score = evaluate(model)     # @task
```

---

## Hands-On: Build an ML Pipeline

### Step 1: Simple pipeline

```python
# pipeline.py
from prefect import flow, task
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib

@task(name="load-data")
def load_data():
    """Load or generate the dataset."""
    np.random.seed(42)
    data = pd.DataFrame({
        "trip_distance": np.random.uniform(1, 20, 1000),
        "passenger_count": np.random.randint(1, 6, 1000),
    })
    data["fare_amount"] = 2.5 + (data["trip_distance"] * 2.8) + np.random.normal(0, 2, 1000)
    print(f"Loaded {len(data)} rows")
    return data

@task(name="preprocess")
def preprocess(data):
    """Clean the data."""
    data = data.dropna()
    data = data[data["trip_distance"] > 0]
    data = data[data["fare_amount"] > 0]
    print(f"After cleaning: {len(data)} rows")
    return data

@task(name="train-model")
def train_model(data):
    """Train a model and return it with test data."""
    X = data[["trip_distance", "passenger_count"]]
    y = data["fare_amount"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LinearRegression()
    model.fit(X_train, y_train)

    return model, X_test, y_test

@task(name="evaluate")
def evaluate(model, X_test, y_test):
    """Evaluate the model and return metrics."""
    preds = model.predict(X_test)
    metrics = {
        "mae": mean_absolute_error(y_test, preds),
        "rmse": np.sqrt(mean_squared_error(y_test, preds)),
        "r2": r2_score(y_test, preds),
    }
    print(f"Metrics: {metrics}")
    return metrics

@task(name="save-model")
def save_model(model, metrics):
    """Save model if quality is good enough."""
    if metrics["r2"] < 0.7:
        raise ValueError(f"Model quality too low: R2 = {metrics['r2']:.4f}")

    joblib.dump(model, "model.pkl")
    print("Model saved to model.pkl")

@flow(name="taxi-fare-pipeline")
def ml_pipeline():
    data = load_data()
    clean_data = preprocess(data)
    model, X_test, y_test = train_model(clean_data)
    metrics = evaluate(model, X_test, y_test)
    save_model(model, metrics)

if __name__ == "__main__":
    ml_pipeline()
```

### Step 2: Run it

```bash
python pipeline.py
```

Prefect will log each task, show timing, and report success/failure.

---

## Adding Retries

Network calls fail. Data sources go down. Retries handle that automatically.

```python
@task(name="load-data", retries=3, retry_delay_seconds=10)
def load_data():
    # If this fails, Prefect will retry up to 3 times
    # with a 10-second delay between attempts
    ...
```

---

## Adding a Schedule

Run your pipeline automatically:

```python
from prefect import flow
from prefect.schedules import CronSchedule

@flow(name="taxi-fare-pipeline")
def ml_pipeline():
    ...

if __name__ == "__main__":
    # Run every day at 6 AM
    ml_pipeline.serve(
        name="daily-training",
        cron="0 6 * * *"
    )
```

Common cron patterns:

| Pattern | Meaning |
|---------|---------|
| `0 6 * * *` | Every day at 6 AM |
| `0 */6 * * *` | Every 6 hours |
| `0 6 * * 1` | Every Monday at 6 AM |
| `*/30 * * * *` | Every 30 minutes |

---

## Prefect UI

Start the Prefect server to get a dashboard:

```bash
prefect server start
```

Open http://localhost:4200. You'll see:
- All flow runs with status (completed, failed, running)
- Task-level details and logs
- Timing for each step
- History of past runs

---

## Adding MLflow Inside a Pipeline

Combine Prefect (orchestration) with MLflow (tracking):

```python
@task(name="train-and-log")
def train_and_log(data):
    import mlflow
    mlflow.set_experiment("taxi-fare-pipeline")

    X = data[["trip_distance", "passenger_count"]]
    y = data["fare_amount"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    with mlflow.start_run():
        model = LinearRegression()
        model.fit(X_train, y_train)
        preds = model.predict(X_test)

        rmse = np.sqrt(mean_squared_error(y_test, preds))
        mlflow.log_param("model_type", "LinearRegression")
        mlflow.log_metric("rmse", rmse)
        mlflow.sklearn.log_model(model, "model")

    return model, X_test, y_test
```

Now every pipeline run automatically logs to MLflow.

---

## Prefect vs Airflow

| Feature | Prefect | Airflow |
|---------|---------|---------|
| Language | Python functions | Python + YAML-like DAG definitions |
| Setup | `pip install prefect` | Needs database, webserver, scheduler |
| Learning curve | Low | Steep |
| Scheduling | Built-in | Built-in (more powerful) |
| UI | Clean, modern | Functional but older |
| Best for | Small-medium teams, getting started | Enterprise, complex dependencies |

Start with Prefect. Move to Airflow later if you need its advanced features.

---

## Key Takeaways

- Pipeline orchestration automates multi-step ML workflows
- Prefect uses plain Python decorators: `@task` and `@flow`
- Add retries to handle failures automatically
- Schedule pipelines to run on a timer
- Combine Prefect (orchestration) with MLflow (tracking) for a complete system

---

## Practice

1. Convert your training workflow into a Prefect pipeline with at least 4 tasks
2. Run it and check the terminal output for task status
3. Add retries to the data loading task
4. Start `prefect server` and view runs in the UI
5. (Bonus) Combine Prefect with MLflow so each pipeline run logs to MLflow

---

Next: [06-model-monitoring.md](06-model-monitoring.md)

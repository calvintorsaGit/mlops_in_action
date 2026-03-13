# Day 5-6: CI/CD for Machine Learning

## The Problem

Every time you change your code, you have to manually:
1. Run tests
2. Retrain the model
3. Check if the model is still good
4. Build a new Docker image
5. Deploy it

This is slow, error-prone, and doesn't scale.

---

## The Solution

**CI/CD** automates all of that.

- **CI (Continuous Integration)** — automatically run tests when you push code
- **CD (Continuous Deployment)** — automatically deploy when tests pass

```
Push code → Run tests → Train model → Check quality → Build image → Deploy
                ↓                          ↓
           If tests fail             If quality drops
           → Stop, alert              → Stop, alert
```

---

## Tool: GitHub Actions

GitHub Actions runs workflows automatically when events happen in your repo (push, pull request, schedule, etc.).

Workflows are defined in `.github/workflows/` as YAML files.

---

## Part 1: What to Test in ML

ML testing is different from regular software testing. You need to test the code, the data, and the model.

| Test type | What it checks | Example |
|-----------|---------------|---------|
| **Unit tests** | Functions work correctly | Does `preprocess()` handle missing values? |
| **Data tests** | Data quality | Does the dataset have expected columns? Are values in range? |
| **Model tests** | Model quality | Is RMSE below 6.0? Is R2 above 0.7? |
| **API tests** | Endpoint works | Does `/predict` return valid JSON? |

---

## Part 2: Write Tests

### Install pytest

```bash
pip install pytest requests
```

### Unit tests

```python
# tests/test_preprocessing.py
import numpy as np
import pandas as pd

def preprocess(df):
    """Clean the dataframe."""
    df = df.dropna()
    df = df[df["trip_distance"] > 0]
    df = df[df["fare_amount"] > 0]
    return df

def test_preprocess_removes_nulls():
    df = pd.DataFrame({
        "trip_distance": [1.0, None, 3.0],
        "fare_amount": [5.0, 10.0, 15.0],
        "passenger_count": [1, 2, 3],
    })
    result = preprocess(df)
    assert result.isnull().sum().sum() == 0

def test_preprocess_removes_zero_distance():
    df = pd.DataFrame({
        "trip_distance": [0.0, 5.0, 10.0],
        "fare_amount": [5.0, 10.0, 15.0],
        "passenger_count": [1, 2, 3],
    })
    result = preprocess(df)
    assert (result["trip_distance"] > 0).all()

def test_preprocess_removes_negative_fare():
    df = pd.DataFrame({
        "trip_distance": [1.0, 5.0, 10.0],
        "fare_amount": [-5.0, 10.0, 15.0],
        "passenger_count": [1, 2, 3],
    })
    result = preprocess(df)
    assert (result["fare_amount"] > 0).all()
```

### Model quality tests

```python
# tests/test_model.py
import joblib
import numpy as np
from sklearn.metrics import mean_squared_error, r2_score

def test_model_quality():
    model = joblib.load("model.pkl")

    # Test data
    np.random.seed(99)
    X_test = np.random.uniform(1, 20, (200, 2))
    y_test = 2.5 + (X_test[:, 0] * 2.8) + np.random.normal(0, 2, 200)

    preds = model.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, preds))
    r2 = r2_score(y_test, preds)

    assert rmse < 6.0, f"RMSE too high: {rmse}"
    assert r2 > 0.7, f"R2 too low: {r2}"

def test_model_output_shape():
    model = joblib.load("model.pkl")
    X = np.array([[5.0, 2], [10.0, 1]])
    preds = model.predict(X)
    assert preds.shape == (2,)

def test_model_predictions_reasonable():
    model = joblib.load("model.pkl")
    X = np.array([[5.0, 2]])
    pred = model.predict(X)[0]
    # A 5-mile trip should cost between $5 and $50
    assert 5.0 < pred < 50.0, f"Prediction out of range: {pred}"
```

### Run tests locally

```bash
pytest tests/ -v
```

---

## Part 3: GitHub Actions Workflow

Create this file in your repo:

```yaml
# .github/workflows/ml-pipeline.yml
name: ML Pipeline

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test-and-train:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.10"

      - name: Install dependencies
        run: pip install -r requirements.txt pytest

      - name: Train model
        run: python save_model.py

      - name: Run tests
        run: pytest tests/ -v

  build-image:
    needs: test-and-train
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.10"

      - name: Install and train
        run: |
          pip install -r requirements.txt
          python save_model.py

      - name: Build Docker image
        run: docker build -t taxi-fare-api .

      # Uncomment below to push to Docker Hub:
      # - name: Login to Docker Hub
      #   uses: docker/login-action@v3
      #   with:
      #     username: ${{ secrets.DOCKER_USERNAME }}
      #     password: ${{ secrets.DOCKER_PASSWORD }}
      #
      # - name: Push image
      #   run: |
      #     docker tag taxi-fare-api ${{ secrets.DOCKER_USERNAME }}/taxi-fare-api:latest
      #     docker push ${{ secrets.DOCKER_USERNAME }}/taxi-fare-api:latest
```

### What this does

1. On every push or PR to `main`:
   - Check out the code
   - Install Python and dependencies
   - Train the model
   - Run all tests
2. If tests pass AND it's a push to `main`:
   - Build the Docker image
   - (Optionally) push to Docker Hub

### How to set up secrets

Go to your GitHub repo → Settings → Secrets and variables → Actions → New repository secret.

Add `DOCKER_USERNAME` and `DOCKER_PASSWORD`.

---

## Part 4: Testing Best Practices for ML

**What makes ML testing different from regular software testing:**

| Regular software | ML software |
|-----------------|-------------|
| Deterministic — same input, same output | Stochastic — outputs can vary |
| Test exact values | Test ranges and distributions |
| Test code logic | Test code logic + data quality + model quality |
| Bugs are in the code | Bugs can be in the code, data, or model |

**Rules of thumb:**

- Always set random seeds in tests for reproducibility
- Test that predictions are within a reasonable range, not exact values
- Test data quality before training (missing values, wrong types, outliers)
- Set minimum quality thresholds for model metrics
- Keep tests fast — use small sample data in CI

---

## Key Takeaways

- CI/CD automates testing and deployment — no manual steps
- ML needs 4 types of tests: unit, data, model, and API
- GitHub Actions runs your pipeline on every push
- Set minimum quality thresholds so bad models never get deployed
- Use secrets for credentials, never hardcode them

---

## Practice

1. Write 3 unit tests for your preprocessing code
2. Write a model quality test with metric thresholds
3. Create a `.github/workflows/ml-pipeline.yml` file
4. Push to GitHub and watch the workflow run in the Actions tab
5. (Bonus) Add Docker build and push steps

---

Next: [04-week1-project.md](04-week1-project.md)

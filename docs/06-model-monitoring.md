# Day 10-11: Model Monitoring and Data Drift

## The Problem

You deploy a model. It works great on day one. Three months later, predictions are garbage but nobody notices until a customer complains.

Models don't stay accurate forever. The world changes, and your model's assumptions stop being true.

---

## Why Models Degrade

| Type | What happens | Example |
|------|-------------|---------|
| **Data drift** | Input data distribution changes | Users start taking longer trips |
| **Concept drift** | Input-output relationship changes | Same distance costs more due to inflation |
| **Model decay** | Combination of both | Predictions slowly get worse |

---

## What to Monitor

| Metric | What it tells you | Alert when |
|--------|-------------------|------------|
| Prediction distribution | Are predictions shifting? | Mean or variance changes |
| Feature distribution | Is input data changing? | Statistical test fails |
| Model accuracy | Is the model still correct? | Below threshold (R2 < 0.7) |
| Response latency | Is the API fast enough? | P95 > 500ms |
| Data quality | Is incoming data valid? | Missing values, wrong types |

---

## Tool: Evidently AI

Compares "reference" data (training) with "current" data (production) and reports drift.

```bash
pip install evidently
```

### Detect drift

```python
import pandas as pd
import numpy as np
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset

np.random.seed(42)

# Reference: what the model trained on
reference = pd.DataFrame({
    "trip_distance": np.random.uniform(1, 15, 1000),
    "passenger_count": np.random.randint(1, 4, 1000),
    "fare_amount": np.random.uniform(5, 50, 1000),
})

# Current: what's coming in now (shifted)
current = pd.DataFrame({
    "trip_distance": np.random.uniform(5, 25, 1000),
    "passenger_count": np.random.randint(1, 6, 1000),
    "fare_amount": np.random.uniform(15, 80, 1000),
})

report = Report(metrics=[DataDriftPreset()])
report.run(reference_data=reference, current_data=current)
report.save_html("data_drift_report.html")
```

### Check drift in code

```python
result = report.as_dict()
drift_detected = result["metrics"][0]["result"]["dataset_drift"]

if drift_detected:
    print("DRIFT DETECTED - retrain the model")
else:
    print("No drift - model is fine")
```

### Automated test suite

```python
from evidently.test_suite import TestSuite
from evidently.tests import TestShareOfDriftedColumns, TestColumnDrift

suite = TestSuite(tests=[
    TestShareOfDriftedColumns(lt=0.3),
    TestColumnDrift(column_name="trip_distance"),
])

suite.run(reference_data=reference, current_data=current)
result = suite.as_dict()

all_passed = all(t["status"] == "SUCCESS" for t in result["tests"])
if not all_passed:
    print("ALERT: Data quality checks failed!")
```

---

## When to Retrain

| Strategy | How it works | When to use |
|----------|-------------|-------------|
| **Scheduled** | Retrain weekly/monthly | Data changes gradually |
| **Triggered** | Retrain when drift detected | Data changes unpredictably |
| **Continuous** | Retrain on every new batch | Data changes constantly |

---

## Key Takeaways

- Models degrade because data and relationships change over time
- Monitor both data drift and model performance
- Evidently AI generates drift reports and automated test suites
- Retrain when performance drops, not just when drift is detected

---

## Practice

1. Create reference and current datasets with obvious drift
2. Generate a drift report with Evidently and view it
3. Write a test suite that checks for drift
4. Modify current data to have no drift and verify tests pass
5. (Bonus) Add monitoring to your Prefect pipeline

---

Next: [07-cloud-deployment.md](07-cloud-deployment.md)

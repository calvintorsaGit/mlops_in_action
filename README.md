# MLOps in Action — 2-Week Learning Pathway

A practical guide to learn MLOps fundamentals in 14 days. No buzzwords, just what you need to know and do.

---

## What is MLOps

MLOps is the process of taking an ML model from your laptop to production, keeping it running, and fixing it when it breaks.

It covers: experiment tracking, packaging, deployment, automation, and monitoring.

Your ML model code is maybe 10% of a production ML system. The other 90% is infrastructure, testing, pipelines, and monitoring. That's what MLOps handles.

---

## Learning Schedule

### Week 1: Foundations

| Day | Topic | Doc |
|-----|-------|-----|
| 1-2 | Experiment Tracking (MLflow) | [01-experiment-tracking.md](docs/01-experiment-tracking.md) |
| 3-4 | Model Packaging (Docker + FastAPI) | [02-model-packaging.md](docs/02-model-packaging.md) |
| 5-6 | CI/CD for ML (GitHub Actions) | [03-ci-cd.md](docs/03-ci-cd.md) |
| 7   | Week 1 Review & Mini Project | [04-week1-project.md](docs/04-week1-project.md) |

### Week 2: Production

| Day | Topic | Doc |
|-----|-------|-----|
| 8-9   | Pipeline Orchestration (Prefect) | [05-pipeline-orchestration.md](docs/05-pipeline-orchestration.md) |
| 10-11 | Model Monitoring & Data Drift | [06-model-monitoring.md](docs/06-model-monitoring.md) |
| 12-13 | Cloud Deployment & Scaling | [07-cloud-deployment.md](docs/07-cloud-deployment.md) |
| 14    | Capstone Project | [08-capstone-project.md](docs/08-capstone-project.md) |

---

## Tools Overview

| Tool | Purpose |
|------|---------|
| MLflow | Track experiments, log metrics, save models |
| DVC | Version control for datasets |
| Docker | Package model + dependencies into a container |
| FastAPI | Serve model as a REST API |
| GitHub Actions | Automate testing and deployment |
| Prefect | Orchestrate multi-step ML workflows |
| Evidently AI | Monitor data drift and model quality |
| AWS / GCP / Azure | Run models in the cloud |

---

## Learning Checklist

Check off each item as you complete it. This is your full pathway from zero to production.

### Fundamentals
- [ ] Understand what MLOps is and why it exists
- [ ] Know the difference between ML in a notebook vs ML in production
- [ ] Set up a Python project with proper structure (src, tests, requirements.txt)

### Experiment Tracking (Day 1-2)
- [ ] Install MLflow
- [ ] Train a model and log parameters, metrics, and artifacts
- [ ] Run `mlflow ui` and view your experiments in the dashboard
- [ ] Compare multiple model runs side by side
- [ ] Register your best model in the MLflow Model Registry
- [ ] Understand model stages: Staging vs Production
- [ ] (Bonus) Set up DVC to version a dataset

### Model Packaging (Day 3-4)
- [ ] Write a FastAPI app that loads a model and serves predictions
- [ ] Test the API locally with curl or a browser
- [ ] Write a Dockerfile for the app
- [ ] Build a Docker image and run it
- [ ] Understand the difference between image and container
- [ ] Push the image to Docker Hub or a registry

### CI/CD (Day 5-6)
- [ ] Write unit tests for your preprocessing and prediction code
- [ ] Write a data validation test (check columns, types, ranges)
- [ ] Write a model quality test (assert metrics are above threshold)
- [ ] Create a GitHub Actions workflow that runs tests on push
- [ ] Add a step to train the model in CI
- [ ] Add a step to build and push the Docker image on success

### Week 1 Review (Day 7)
- [ ] Build one project that combines: MLflow + Docker + FastAPI + GitHub Actions
- [ ] Push it to GitHub with a working CI pipeline
- [ ] Someone else can clone it, run it, and get predictions

### Pipeline Orchestration (Day 8-9)
- [ ] Install Prefect
- [ ] Convert your ML workflow into tasks and flows
- [ ] Run a pipeline that does: load data -> preprocess -> train -> evaluate
- [ ] View your pipeline runs in the Prefect UI
- [ ] Add error handling and retries to tasks
- [ ] (Bonus) Schedule a pipeline to run daily

### Model Monitoring (Day 10-11)
- [ ] Understand data drift, concept drift, and model decay
- [ ] Install Evidently AI
- [ ] Generate a data drift report comparing training data vs new data
- [ ] Generate a model performance report
- [ ] Know when to retrain: set up threshold-based alerts
- [ ] (Bonus) Set up Grafana dashboard for live monitoring

### Cloud Deployment (Day 12-13)
- [ ] Understand the basics of cloud platforms (AWS, GCP, Azure)
- [ ] Deploy a Docker container to a cloud service (e.g., AWS ECS, GCP Cloud Run)
- [ ] Understand deployment strategies: blue-green, canary, shadow
- [ ] Know what Kubernetes does (don't need to master it yet)
- [ ] Set up a load balancer in front of your model API

### Capstone (Day 14)
- [ ] Build an end-to-end MLOps pipeline with all the pieces connected
- [ ] Version data with DVC
- [ ] Track experiments with MLflow
- [ ] Orchestrate with Prefect
- [ ] Package with Docker
- [ ] Automate with GitHub Actions
- [ ] Serve with FastAPI
- [ ] Monitor with Evidently

---

## How to Use This Guide

1. Read the docs in order. Each one builds on the previous.
2. Type the code yourself. Don't copy-paste.
3. Break things on purpose. That's how you learn what each piece does.
4. Use one project throughout — build a taxi fare predictor from Day 1 to Day 14.

---

## Resources

| Resource | Type | URL |
|----------|------|-----|
| MLOps Zoomcamp | Free Course | https://github.com/DataTalksClub/mlops-zoomcamp |
| Made With ML | Free Course | https://madewithml.com |
| Full Stack Deep Learning | Course | https://fullstackdeeplearning.com |
| Designing ML Systems (Chip Huyen) | Book | https://www.oreilly.com/library/view/designing-machine-learning/9781098107956/ |
| MLflow Docs | Docs | https://mlflow.org/docs/latest |

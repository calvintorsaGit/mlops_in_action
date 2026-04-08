# MLOps in Action — 4-Week Learning Pathway

A practical guide to learn production-grade MLOps in 28 days. Covers the full stack: experiment tracking, packaging, cloud deployment, Kubernetes, model serving with KServe, managed ML with SageMaker, and pipeline orchestration with Kubeflow.

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

### Week 2: Production Pipelines

| Day | Topic | Doc |
|-----|-------|-----|
| 8-9   | Pipeline Orchestration (Prefect) | [05-pipeline-orchestration.md](docs/05-pipeline-orchestration.md) |
| 10-11 | Model Monitoring & Data Drift | [06-model-monitoring.md](docs/06-model-monitoring.md) |
| 12-13 | Cloud Deployment & Scaling (AWS ECS / GCP Cloud Run) | [07-cloud-deployment.md](docs/07-cloud-deployment.md) |
| 14    | Week 2 Capstone | [08-capstone-project.md](docs/08-capstone-project.md) |

### Week 3: Kubernetes & Model Serving

| Day | Topic | Doc |
|-----|-------|-----|
| 15-16 | Kubernetes Fundamentals (Pods, Deployments, Services) | [09-kubernetes-fundamentals.md](docs/09-kubernetes-fundamentals.md) |
| 17-18 | Deploy ML Model on Kubernetes (kubectl, Helm) | [10-kubernetes-ml-deploy.md](docs/10-kubernetes-ml-deploy.md) |
| 19-20 | KServe — Production Model Serving on K8s | [11-kserve.md](docs/11-kserve.md) |
| 21    | Week 3 Review & KServe Mini Project | [12-week3-project.md](docs/12-week3-project.md) |

### Week 4: Managed ML Platforms

| Day | Topic | Doc |
|-----|-------|-----|
| 22-23 | AWS SageMaker — Training, Registry & Endpoints | [13-sagemaker.md](docs/13-sagemaker.md) |
| 24-25 | Kubeflow — ML Pipelines at Scale | [14-kubeflow.md](docs/14-kubeflow.md) |
| 26-27 | DVC Advanced — Data Versioning & Remote Storage | [15-dvc-advanced.md](docs/15-dvc-advanced.md) |
| 28    | Final Capstone — End-to-End Production MLOps | [16-final-capstone.md](docs/16-final-capstone.md) |

---

## Tools Overview

| Tool | Purpose | Week |
|------|---------|------|
| MLflow | Track experiments, log metrics, save models | 1 |
| DVC | Version control for datasets and models | 1 & 4 |
| Docker | Package model + dependencies into a container | 1 |
| FastAPI | Serve model as a REST API | 1 |
| GitHub Actions | Automate testing and deployment | 1 |
| Prefect | Orchestrate multi-step ML workflows | 2 |
| Evidently AI | Monitor data drift and model quality | 2 |
| AWS / GCP / Azure | Run models in the cloud | 2 |
| Kubernetes (K8s) | Manage and scale containerized workloads | 3 |
| KServe | Production-grade model serving on Kubernetes | 3 |
| AWS SageMaker | Managed ML platform: training, tuning, deployment | 4 |
| Kubeflow | End-to-end ML pipelines on Kubernetes | 4 |

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
- [ ] Run a pipeline that does: load data → preprocess → train → evaluate
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

### Week 2 Capstone (Day 14)
- [ ] Build an end-to-end MLOps pipeline with all the pieces connected
- [ ] Version data with DVC
- [ ] Track experiments with MLflow
- [ ] Orchestrate with Prefect
- [ ] Package with Docker
- [ ] Automate with GitHub Actions
- [ ] Serve with FastAPI
- [ ] Monitor with Evidently

### Kubernetes Fundamentals (Day 15-16)
- [ ] Understand Kubernetes architecture: control plane, nodes, pods
- [ ] Install `kubectl` and connect to a cluster (use Minikube or Kind locally)
- [ ] Deploy your Docker image as a Kubernetes Deployment
- [ ] Expose it with a Kubernetes Service
- [ ] Scale pods up and down manually
- [ ] Understand resource requests and limits (CPU, memory)
- [ ] Understand ConfigMaps and Secrets

### Kubernetes ML Deployment (Day 17-18)
- [ ] Package your ML app with Helm charts
- [ ] Deploy to a real cluster (EKS, GKE, or AKS)
- [ ] Set up Horizontal Pod Autoscaler (HPA) for auto-scaling
- [ ] Set up health checks (readiness and liveness probes)
- [ ] Roll out a new model version with zero downtime
- [ ] (Bonus) Use Ingress + TLS for public HTTPS endpoint

### KServe (Day 19-20)
- [ ] Understand what KServe is and how it differs from plain Kubernetes
- [ ] Install KServe on a Kubernetes cluster (or use a managed version)
- [ ] Deploy an MLflow model using a KServe `InferenceService`
- [ ] Send prediction requests to the KServe endpoint
- [ ] Understand Canary rollouts in KServe
- [ ] Enable model explainability with KServe explainers
- [ ] (Bonus) Enable request batching and autoscaling with KServe

### Week 3 Review (Day 21)
- [ ] Deploy your taxi fare model on Kubernetes via KServe
- [ ] Set up canary deployment switching between two model versions
- [ ] Document your cluster setup in code (YAML / Helm)

### AWS SageMaker (Day 22-23)
- [ ] Understand SageMaker's core concepts: Training Jobs, Models, Endpoints
- [ ] Set up AWS credentials and SageMaker Studio
- [ ] Run a training job on SageMaker using a built-in algorithm
- [ ] Register a trained model in the SageMaker Model Registry
- [ ] Deploy a real-time inference endpoint
- [ ] Run batch transform jobs for large-scale predictions
- [ ] Understand SageMaker Pipelines for automated retraining
- [ ] (Bonus) Use SageMaker Experiments to track runs (vs MLflow)

### Kubeflow (Day 24-25)
- [ ] Understand Kubeflow's components: Pipelines, Katib, KFServing
- [ ] Install Kubeflow on a Kubernetes cluster (or use Kubeflow on GKE)
- [ ] Build a Kubeflow Pipeline with Python SDK (`kfp`)
- [ ] Run a pipeline: data ingest → preprocess → train → evaluate → deploy
- [ ] Use Kubeflow Katib for hyperparameter tuning
- [ ] Understand the difference between Kubeflow Pipelines and Prefect/Airflow
- [ ] (Bonus) Integrate Kubeflow with MLflow for experiment tracking

### DVC Advanced (Day 26-27)
- [ ] Set up DVC with a remote storage backend (S3, GCS, or Azure Blob)
- [ ] Version datasets and push/pull from remote
- [ ] Build a DVC pipeline (`dvc.yaml`) for reproducible ML workflows
- [ ] Use `dvc repro` to reproduce the full pipeline
- [ ] Compare metrics across DVC experiments with `dvc metrics diff`
- [ ] Integrate DVC pipelines with GitHub Actions for CI/CD
- [ ] (Bonus) Use DVC Studio for team experiment visibility

### Final Capstone (Day 28)
- [ ] Build a fully production-grade MLOps system from scratch
- [ ] Version data with DVC (remote S3 storage)
- [ ] Track experiments with MLflow
- [ ] Build retraining pipelines with Kubeflow or Prefect
- [ ] Package with Docker
- [ ] Deploy on Kubernetes with KServe or SageMaker endpoint
- [ ] Automate everything with GitHub Actions CI/CD
- [ ] Monitor with Evidently + Grafana
- [ ] Write a technical README documenting the full architecture

---

## How to Use This Guide

1. Read the docs in order. Each one builds on the previous.
2. Type the code yourself. Don't copy-paste.
3. Break things on purpose. That's how you learn what each piece does.
4. Use one project throughout — build a taxi fare predictor from Day 1 to Day 28.

---

## Resources

| Resource | Type | URL |
|----------|------|-----|
| MLOps Zoomcamp | Free Course | https://github.com/DataTalksClub/mlops-zoomcamp |
| Made With ML | Free Course | https://madewithml.com |
| Full Stack Deep Learning | Course | https://fullstackdeeplearning.com |
| Designing ML Systems (Chip Huyen) | Book | https://www.oreilly.com/library/view/designing-machine-learning/9781098107956/ |
| MLflow Docs | Docs | https://mlflow.org/docs/latest |
| Kubernetes Docs | Docs | https://kubernetes.io/docs/home/ |
| KServe Docs | Docs | https://kserve.github.io/website/ |
| AWS SageMaker Docs | Docs | https://docs.aws.amazon.com/sagemaker/ |
| Kubeflow Docs | Docs | https://www.kubeflow.org/docs/ |
| DVC Docs | Docs | https://dvc.org/doc |

# Day 12-13: Cloud Deployment and Scaling

## The Problem

Your Docker container works on your laptop. But where do you actually run it so real users can access it? And what happens when 1000 users send requests at the same time?

---

## Cloud Platforms

| Platform | ML Service | Free tier |
|----------|-----------|-----------|
| **AWS** | SageMaker | Limited |
| **GCP** | Vertex AI | $300 credit |
| **Azure** | Azure ML | $200 credit |

You don't need to master all three. Pick one and learn its basics.

---

## Simplest Deployment: GCP Cloud Run

Cloud Run takes a Docker container and runs it as a web service. You don't manage servers.

### Steps

```bash
# 1. Install gcloud CLI
# Download from https://cloud.google.com/sdk/docs/install

# 2. Login and set project
gcloud auth login
gcloud config set project YOUR_PROJECT_ID

# 3. Build and push image to Google Container Registry
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/taxi-fare-api

# 4. Deploy to Cloud Run
gcloud run deploy taxi-fare-api \
  --image gcr.io/YOUR_PROJECT_ID/taxi-fare-api \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

That's it. You get a public URL like `https://taxi-fare-api-xxxxx.run.app`.

### AWS Equivalent (ECS + Fargate)

```bash
# 1. Push image to ECR (Elastic Container Registry)
aws ecr create-repository --repository-name taxi-fare-api
docker tag taxi-fare-api:latest AWS_ACCOUNT_ID.dkr.ecr.REGION.amazonaws.com/taxi-fare-api
docker push AWS_ACCOUNT_ID.dkr.ecr.REGION.amazonaws.com/taxi-fare-api

# 2. Create an ECS service with Fargate (serverless containers)
# Usually done through AWS Console or Terraform for first-time setup
```

---

## Deployment Strategies

When updating a model in production, don't just swap it. Use a safe strategy.

| Strategy | How it works | Risk |
|----------|-------------|------|
| **Blue-Green** | Run old and new side by side, switch traffic | Low |
| **Canary** | Send 5% traffic to new model, increase gradually | Low |
| **Shadow** | Run new model in parallel, compare but don't serve its results | Very Low |
| **A/B Testing** | Split users between models, measure business impact | Medium |

### Canary example

```
Day 1:  95% → old model,  5% → new model  (check metrics)
Day 2:  80% → old model, 20% → new model  (still good?)
Day 3:  50% → old model, 50% → new model  (looking good)
Day 4: 100% → new model                   (fully rolled out)
```

If the new model performs badly at any step, roll back to 100% old model.

---

## Kubernetes (The Basics)

Kubernetes (K8s) manages containers at scale. You don't need to master it now, but understand what it does.

| Concept | What it is |
|---------|-----------|
| **Pod** | The smallest unit — one or more containers running together |
| **Deployment** | Manages a group of identical pods |
| **Service** | Exposes pods to the network (load balancer) |
| **Scaling** | Automatically add/remove pods based on load |

```
User requests
      |
  [Load Balancer]
   /    |    \
Pod1  Pod2  Pod3    ← same model, different instances
```

When load increases, Kubernetes adds more pods. When it decreases, it removes them.

### Basic Kubernetes deployment file

```yaml
# k8s-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: taxi-fare-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: taxi-fare-api
  template:
    metadata:
      labels:
        app: taxi-fare-api
    spec:
      containers:
        - name: taxi-fare-api
          image: yourusername/taxi-fare-api:v1
          ports:
            - containerPort: 8000
          resources:
            requests:
              memory: "256Mi"
              cpu: "250m"
            limits:
              memory: "512Mi"
              cpu: "500m"
```

---

## Infrastructure as Code

Don't click through cloud consoles to set things up. Define your infrastructure in code so it's reproducible.

| Tool | What it does |
|------|-------------|
| **Terraform** | Define cloud resources in config files |
| **Pulumi** | Same but using Python/TypeScript |
| **AWS CDK** | AWS-specific, uses Python/TypeScript |

This is good to know about but not critical for your first 2 weeks.

---

## Key Takeaways

- Cloud Run (GCP) or ECS Fargate (AWS) are the simplest ways to deploy
- Use canary or blue-green deployments to reduce risk
- Kubernetes manages containers at scale but has a steep learning curve
- Infrastructure as Code keeps your setup reproducible

---

## Practice

1. Deploy your Docker container to GCP Cloud Run or AWS ECS
2. Test the public URL with curl
3. Read about canary deployments and understand the concept
4. Look at a Kubernetes deployment file and understand what each field does
5. (Bonus) Set up auto-scaling based on CPU usage

---

Next: [08-capstone-project.md](08-capstone-project.md)

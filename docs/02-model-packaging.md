# Day 3-4: Model Packaging

## The Problem

Your model works on your laptop. Your teammate tries to run it and gets dependency errors. You deploy it to a server and it crashes because the server has a different Python version.

"It works on my machine" is not a deployment strategy.

---

## The Solution

Package your model, its code, and all its dependencies into a container. The container runs the same way everywhere — your laptop, your teammate's laptop, a cloud server, anywhere.

---

## Part 1: Serve Your Model with FastAPI

Before containerizing, you need a way for people to send data and get predictions back. That's an API.

**FastAPI** lets you build one in a few lines of code.

### Install

```bash
pip install fastapi uvicorn joblib scikit-learn
```

### Create the API

```python
# app.py
from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np

app = FastAPI()

# Load the trained model
model = joblib.load("model.pkl")

# Define what the request looks like
class TripInput(BaseModel):
    trip_distance: float
    passenger_count: int

# Define the prediction endpoint
@app.post("/predict")
def predict(trip: TripInput):
    features = np.array([[trip.trip_distance, trip.passenger_count]])
    prediction = model.predict(features)
    return {"fare_amount": round(float(prediction[0]), 2)}

# Health check
@app.get("/health")
def health():
    return {"status": "ok"}
```

### Save your model first

```python
# save_model.py
import joblib
from sklearn.linear_model import LinearRegression
import numpy as np

np.random.seed(42)
X = np.random.uniform(1, 20, (1000, 2))
y = 2.5 + (X[:, 0] * 2.8) + np.random.normal(0, 2, 1000)

model = LinearRegression()
model.fit(X, y)
joblib.dump(model, "model.pkl")
print("Model saved.")
```

### Run the API

```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

### Test it

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"trip_distance": 5.0, "passenger_count": 2}'
```

Or open http://localhost:8000/docs — FastAPI gives you an interactive API page for free.

---

## Part 2: Containerize with Docker

### Key Concepts

| Term | What it is |
|------|-----------|
| **Dockerfile** | A text file with instructions to build your container |
| **Image** | A snapshot built from the Dockerfile. Like a frozen meal. |
| **Container** | A running instance of an image. Like serving the meal. |
| **Registry** | A storage service for images (Docker Hub, AWS ECR, etc.) |

### How it works

```
Your code + dependencies
        |
        v
   [ Dockerfile ]  -- instructions to build
        |
        v
   [ Docker Image ] -- frozen snapshot
        |
        v
   [ Container ]    -- running instance
```

### Install Docker

Download from https://docs.docker.com/get-docker/

### Write the Dockerfile

```dockerfile
# Dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy code and model
COPY app.py .
COPY model.pkl .

# Expose the port
EXPOSE 8000

# Run the API
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Create requirements.txt

```
fastapi
uvicorn
joblib
scikit-learn
numpy
```

### Build the image

```bash
docker build -t taxi-fare-api .
```

This reads the Dockerfile, installs everything, and creates an image called `taxi-fare-api`.

### Run the container

```bash
docker run -p 8000:8000 taxi-fare-api
```

`-p 8000:8000` maps port 8000 inside the container to port 8000 on your machine.

Now hit http://localhost:8000/predict — same API, but running inside a container.

---

## Part 3: Useful Docker Commands

```bash
# List images
docker images

# List running containers
docker ps

# Stop a container
docker stop <container_id>

# Remove a container
docker rm <container_id>

# Remove an image
docker rmi taxi-fare-api

# View container logs
docker logs <container_id>

# Run container in background
docker run -d -p 8000:8000 taxi-fare-api

# Open a shell inside a running container
docker exec -it <container_id> /bin/bash
```

---

## Part 4: Push to a Registry

Once your image works, push it to Docker Hub so others (or your CI/CD pipeline) can pull it.

```bash
# Login to Docker Hub
docker login

# Tag the image
docker tag taxi-fare-api yourusername/taxi-fare-api:v1

# Push it
docker push yourusername/taxi-fare-api:v1
```

Anyone can now run your model with:

```bash
docker pull yourusername/taxi-fare-api:v1
docker run -p 8000:8000 yourusername/taxi-fare-api:v1
```

---

## Project Structure

After this section, your project should look like:

```
mlops_in_action/
├── app.py                  # FastAPI prediction server
├── save_model.py           # Script to train and save model
├── model.pkl               # Saved model file
├── Dockerfile              # Container instructions
├── requirements.txt        # Python dependencies
└── docs/
    ├── 01-experiment-tracking.md
    └── 02-model-packaging.md
```

---

## Key Takeaways

- FastAPI turns your model into an API endpoint
- Docker packages everything so it works the same everywhere
- Image = frozen snapshot, Container = running instance
- Push images to a registry so anyone can pull and run them

---

## Practice

1. Create a FastAPI app that serves predictions from a trained model
2. Test it locally with curl or the /docs page
3. Write a Dockerfile, build the image, run the container
4. Verify the API works inside the container
5. (Bonus) Push the image to Docker Hub

---

Next: [03-ci-cd.md](03-ci-cd.md)

import mlflow
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import uvicorn

app = FastAPI(title="Taxi Fare Prediction Service")

# Set tracking URI to your local mlruns folder (where you ran your experiments)
mlflow.set_tracking_uri("file:C:/Users/calvinsatriators/Documents/mlops_in_action/implementation/experiment-tracking/mlruns")

# Load the model from the registry once at startup
MODEL_NAME = "taxi-fare-model"
MODEL_ALIAS = "production"

try:
    print(f"Loading model '{MODEL_NAME}' (alias: {MODEL_ALIAS})...")
    model_uri = f"models:/{MODEL_NAME}@{MODEL_ALIAS}"
    model = mlflow.pyfunc.load_model(model_uri)
    print("Model loaded successfully!")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

# Define the input format using Pydantic
class TaxiTrip(BaseModel):
    trip_distance: float
    passenger_count: int

@app.get("/health")
def health():
    return {"status": "ok", "model_version": MODEL_ALIAS}

@app.post("/predict")
def predict(trip: TaxiTrip):
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    # Convert input to DataFrame for MLflow model
    data = pd.DataFrame([trip.dict()])
    
    prediction = model.predict(data)
    
    return {
        "prediction": round(float(prediction[0]), 2),
        "currency": "USD"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

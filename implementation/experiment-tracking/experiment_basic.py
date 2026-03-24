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

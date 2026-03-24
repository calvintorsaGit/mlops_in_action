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

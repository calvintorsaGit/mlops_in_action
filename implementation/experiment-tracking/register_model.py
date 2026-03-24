import mlflow
from mlflow.tracking import MlflowClient
mlflow.set_tracking_uri("mlruns")

# 1. Search for the best run
client = MlflowClient()
experiment = client.get_experiment_by_name("taxi-fare-v1")
if experiment:
    runs = client.search_runs(
        experiment_ids=[experiment.experiment_id],
        order_by=["metrics.rmse ASC"],
        max_results=1
    )
    
    if runs:
        best_run = runs[0]
        run_id = best_run.info.run_id
        rmse = best_run.data.metrics["rmse"]
        print(f"Best run found: {run_id} with RMSE: {rmse}")
        
        # 2. Register the model
        model_uri = f"runs:/{run_id}/model"
        name = "taxi-fare-model"
        print(f"Registering model: {name}")
        result = mlflow.register_model(model_uri, name)
        
        # 3. Promote to production using an ALIAS (since Stages are deprecated in new MLflow)
        print(f"Setting alias 'production' to version {result.version}")
        client.set_registered_model_alias(
            name=name,
            alias="production",
            version=result.version
        )
        print("Done!")
    else:
        print("No runs found in experiment.")
else:
    print("Experiment 'taxi-fare-v1' not found.")

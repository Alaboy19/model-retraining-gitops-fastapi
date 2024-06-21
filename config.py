import os

PROD_ALIAS = "prod"
REGISTERED_MODEL_NAME = "mlops-project-model"
OWNER_NAME = "Alaboy19"
REPOS_NAME = "model-retrain-gitops-fastapi"
EVENT_TYPE = "retrain_pipeline"

# put the correct service URI from the endpoint provided from step hosting MLflow on GCP, where whatever MLflow regsitry URI you have 
os.environ["MLFLOW_TRACKING_URI"] = "https://my-cloud-run-service-1-{something_here}.a.run.app"



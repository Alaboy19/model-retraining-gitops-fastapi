import os

PROD_ALIAS = "prod"
REGISTERED_MODEL_NAME = "mlops-project-model"
GITLAB_PROJECT_NAME = "hardml/mlops-project-solution"
OWNER_NAME = "Alaboy19"
REPOS_NAME = "model-retrain-gitops-fastapi"
EVENT_TYPE = "retrain_pipeline"

os.environ["MLFLOW_TRACKING_URI"] = "https://my-cloud-run-service-1-um3dh5zufa-uc.a.run.app"
os.environ["AWS_ENDPOINT_URL"] = "https://storage.yandexcloud.net"


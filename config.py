import os

PROD_ALIAS = "prod"
REGISTERED_MODEL_NAME = "mlops-project-model"
GITLAB_PROJECT_NAME = "hardml/mlops-project-solution"

os.environ["MLFLOW_TRACKING_URI"] = "https://lab-mlflow.karpov.courses"
os.environ["AWS_ENDPOINT_URL"] = "https://storage.yandexcloud.net"


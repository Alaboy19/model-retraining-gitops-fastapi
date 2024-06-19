import os
import sys
import mlflow
import pandas as pd
from evidently.test_preset import DataDriftTestPreset
from evidently.test_suite import TestSuite
from mlflow import MlflowClient
from sklearn.ensemble import RandomForestRegressor
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.pipeline import Pipeline

from config import PROD_ALIAS, REGISTERED_MODEL_NAME

EXPERIMENT_NAME = "mlops-project"
GOOD_DATA_URL = (
    "https://s3.lab.karpov.courses/mlops-training-sets/project/example/good.csv"
)
# for e in (
#     "MLFLOW_TRACKING_USERNAME",
#     "MLFLOW_TRACKING_PASSWORD",
#     "AWS_ACCESS_KEY_ID",
#     "AWS_SECRET_ACCESS_KEY",
# ):
#     if e not in os.environ:
#         raise ValueError(f"please set {e} env variable")

os.environ["MLFLOW_TRACKING_URI"] = "https://my-cloud-run-service-1-um3dh5zufa-uc.a.run.app"
os.environ["AWS_ENDPOINT_URL"] = "https://storage.yandexcloud.net"


def get_data(): 
    if len(sys.argv) < 2:
        raise ValueError("provide path to data")
    path = sys.argv[1]
    return pd.read_csv(path)


def get_model(params: dict | None):
    params = params or {"model": "rf", "ngrams": {"min": 1, "max": 3}}
    if params["model"] == "linear":
        model = LinearRegression()
    elif params["model"] == "rf":
        model = RandomForestRegressor()
    elif params["model"] == "ridge":
        model = Ridge()
    else:
        raise ValueError()

    # Create the pipeline
    pipeline = Pipeline(
        [
            (
                "vect",
                CountVectorizer(
                    ngram_range=(params["ngrams"]["min"], params["ngrams"]["max"]),
                    analyzer="char",
                ),
            ),
            ("tfidf", TfidfTransformer()),
            ("clf", model),
        ]
    )
    return pipeline


def check_data(df: pd.DataFrame) -> bool:
    reference = pd.read_csv(GOOD_DATA_URL)
    suite = TestSuite(tests=[DataDriftTestPreset(columns=["Times"])])
    suite.run(reference_data=reference, current_data=df)
    return bool(suite)


def main():
    data = get_data()
    if not check_data(data):
        print("Data is bad")
        sys.exit(1)

    model = get_model(None)
    model.fit(data["Password"], data["Times"])

    print(model.predict(data["Password"])[0])

    exp = mlflow.get_experiment_by_name(EXPERIMENT_NAME)
    if exp is None:
        experiment_id = mlflow.create_experiment(EXPERIMENT_NAME)
    else:
        experiment_id = exp.experiment_id
    with mlflow.start_run(experiment_id=experiment_id):
        model = mlflow.sklearn.log_model(model, artifact_path="model")
        reg_model = mlflow.register_model(
            model_uri=model.model_uri, name=REGISTERED_MODEL_NAME
        )
        client = MlflowClient()
        client.set_registered_model_alias(
            REGISTERED_MODEL_NAME, PROD_ALIAS, reg_model.version
        )


if __name__ == "__main__":
    main()

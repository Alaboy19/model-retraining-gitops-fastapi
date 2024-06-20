import os
from typing import Annotated, List
import requests
import mlflow
import uvicorn
from fastapi import Body, Depends, FastAPI
from pydantic import BaseModel, Field

from config import EVENT_TYPE, GITLAB_PROJECT_NAME, OWNER_NAME, PROD_ALIAS, REGISTERED_MODEL_NAME, REPOS_NAME

app = FastAPI()

for e in (
    "GITHUB_TOKEN",
):
    if e not in os.environ:
        raise ValueError(f"please set {e} env variable")


GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]


class PredictRequest(BaseModel):
    passwords: List[str] = Field(alias="Password")


class PredictResponse(BaseModel):
    prediction: List[float] = Field(alias="Times")


_model = None


def get_model():
    global _model
    if _model is None:
        _reload_model()
    return _model


@app.post("/predict")
def predict(
    data: Annotated[PredictRequest, Body()], model=Depends(get_model)
) -> PredictResponse:
    prediction = model.predict(data.passwords)
    return PredictResponse(Times=prediction)


def _reload_model():
    global _model
    _model = mlflow.sklearn.load_model(f"models:/{REGISTERED_MODEL_NAME}@{PROD_ALIAS}")


@app.post("/reload-model")
def reload_model():
    _reload_model()


class Trigger(BaseModel):
    data_url: str


@app.post("/trigger")
def trigger_pipeline():
    url = f"https://api.github.com/repos/{OWNER_NAME}/{REPOS_NAME}/dispatches"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {"event_type": EVENT_TYPE}

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 204:
        print(f"Workflow triggered successfully!")
    else:
        print(f"Error triggering workflow: {response.status_code} - {response.text}")


@app.get("/health")
def health():
    return "OK"


def main():
    uvicorn.run(app, host="0.0.0.0")


if __name__ == "__main__":
    main()

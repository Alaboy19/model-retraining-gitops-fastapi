# model-retrain-gitops-fastapi
This is a one scenario of ML model retraining pipeline performed with GitOps tools, GitHub Actions. Usually, model retraining is needed either by some trigger conditions such as data drift or some regular retraining pipeline every week(or so) for concept drifts. Both options are considered in this pipeline. Generally, this tiny self hosted emulation of system design for MLOps that is based on the best-practice recommendations from Google MLops https://cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning

## Flowchart of the system ## 
![image](https://github.com/Alaboy19/model-retrain-gitops-fastapi/assets/47283347/fbc5aae8-3b17-41d4-bf90-74007c32dc69)

## Some key points considered ##

### MLflow ###
- provides experiment logging
- general access to model artifacts for data scientists
- model reproducability and versioning
- assesing and comparing models based on metrics
- assigning aliases for models that ready for different environment such as dev, prod
  
### FastAPI ###
- lightweight, simple and fast protocol that works async with ASGI server Uvicorn
- compatable with type hints in pyhthon
- integrated with Pydantic for convinent data types validation
- integrated with OpenAPI, automaticlaly generating the API docs and Swagger interface under the box in route /docs
  
### CI-CD ###
- Since it is online serving, there is need for fast packaging and deployment of the service to prod, therefore CI-CD is better option than orchestrators such as Ariflow, Prefect
- Any pushes or pull request must be tested before shipping to prodution, CI-CD is better option there as well
- Orchestrators could be used further for preparing the data for feature store as a abstraction from data engineerin
  
### render ###
- Free way of virtual machines that lets to deploy service from image for docker registry

## Steps taken to develop the pipeline ##
1. Reproduce the ml deployment on render with fastapi serving here https://github.com/Alaboy19/model-serving-github-actions-render, since it is one of the fundamental blocks of this pipeline.
2. Host the mlflow registry somewhere, in this case it is hosted on GCP following the [tutorial](https://medium.com/@andrevargas22/how-to-launch-an-mlflow-server-with-continuous-deployment-on-gcp-in-minutes-7d3a29feff88).
3. The /trigger route was added to webservice that will trigger the gitub actions workflow externally, with github API.
4. The /reload-model that gets the last model that assigned with alias of @prod on mlflow
5. train.py scripts that gets the new_data from static source and checks for data drift, if there is any, it launches the training and pushes the new model with alias to @prod to mlflow registry
6. retrain.ci-cd.yaml that executes all the steps for retraining
## Steps to reproduce the code ## 
1. Either activate a venv and install dependencies with ``` pip install -q -r requriements.txt
``` OR you can install poetry and run ```poetry install```
2. Generate token for access to your dockerhub account 
3. On github actions serctets → add repo secrets for DATA_URL, HOT_RELOAD_URL(route to /reload-model)
4. Also, generate REPO_TOKEN as a acess to your repo and add it to your repo variables in action, it is needed to authentificate to your repo when requesting the trigger of retrain.yml externally from fasdtapi service on render
5. Also, add MLFLOW_TRACKING_URI that got from GCP to repo variables 
6. Follow along the .github.workflows.ci-cd.yml and retrain.yml files
7. If scheduled retraining and redeploy is needed, uncomment the cron shedule in .github/workflows/retrain.yml

## MLOps mature best-practices as reference ## 
![image](https://github.com/Alaboy19/model-retraining-gitops-fastapi/assets/47283347/64412c18-9fd3-47d0-b724-07b9f5d889be)


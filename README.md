# model-retrain-gitops-fastapi
This is a one scenario of ML model retraining pipeline performed with GitOps tools, GitHub Actions. Usually, model retraining is needed either by some trigger conditions such as data drift or some regular retraining pipeline every week(or so) for concept drifts. Both options are considered in this pipeline. Generally, this tiny self hosted emulation of system design for MLOps that is based on the best-practice recommendations from Google MLops https://cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning

## Flowchart of the system ## 
![image](https://github.com/Alaboy19/model-retrain-gitops-fastapi/assets/47283347/fbc5aae8-3b17-41d4-bf90-74007c32dc69)

## Some key points considered ##
- It is better to reproduce first the ml deployment on render with fastapi serving here https://github.com/Alaboy19/model-serving-github-actions-render, since it is the fundamental blocks of this pipeline.

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

## Steps to reproduce the workflow ##

## Steps to reproduce the code ## 
the full pipeline for model retraining with fastapi and github actions

## MLOps mature best-practices as reference ## 
![image](https://github.com/Alaboy19/model-retraining-gitops-fastapi/assets/47283347/64412c18-9fd3-47d0-b724-07b9f5d889be)


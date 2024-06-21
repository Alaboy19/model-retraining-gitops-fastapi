# model-retrain-gitops-fastapi
This is a one scenario of ML model retraining pipeline performed with GitOps tools, GitHub Actions. Usually, model retraining is needed either by some trigger conditions such as data drift or some regular retraining pipeline every week(or so) for concept drifts. Both options are considered in this pipeline. Generally, this tiny self hosted emulation of system design for MLOps that is based on the best-practice recommendations from Google MLops https://cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning
## Some key points considered ##
- It is better to reproduce first the ml deployment on render with fastapi serving here https://github.com/Alaboy19/model-serving-github-actions-render, since it is the fundamental blocks of this pipeline.
- Oneline serving vs Batch processing
- why fastapi
- why render
- why mlflow, provides experiment logging and general access to model artifacts, model reproducability and versioning, assesing and comparing models based on metrics 
- why hosting in gcp
- future work  
## Steps to reproduce the workflow ##

## Steps to reproduce the code ## 
the full pipeline for model retraining with fastapi and github actions
## Flowchart of the system ## 
![image](https://github.com/Alaboy19/model-retrain-gitops-fastapi/assets/47283347/fbc5aae8-3b17-41d4-bf90-74007c32dc69)

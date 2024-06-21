# model-retrain-gitops-fastapi
This is a one scenario where ML model retraining pipeline is performed with GitOps tools, GitHub Actions. Usually, model retraining is needed either by some trigger conditions such as data drift or some regular retraining pipeline every week(or so) for concept drifts. Both options are considered in this pipeline. 
## Some key points considered ##
- It is better to reproduce first the ml deployment on render with fastapi serving here https://github.com/Alaboy19/model-serving-github-actions-render, since it is the fundamental blocks of this pipeline.
- Oneline serving vs Batch processing
- why fastapi
- why render
- why mlflow
- why hosting in gcp
- future work  
## Steps to reproduce the workflow ##

## Steps to reproduce the code ## 
the full pipeline for model retraining with fastapi and github actions
## Flowchart of the system ## 
![image](https://github.com/Alaboy19/model-retrain-gitops-fastapi/assets/47283347/fbc5aae8-3b17-41d4-bf90-74007c32dc69)

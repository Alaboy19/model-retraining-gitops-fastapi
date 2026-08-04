

# Pipeline de reentrenamiento de modelos con GitOps y FastAPI
Este es un escenario de pipeline de reentrenamiento de modelos de ML realizado con herramientas de GitOps y GitHub Actions. Por lo general, el reentrenamiento de modelos es necesario ya sea por ciertas condiciones desencadenantes, como el desfase de datos (data drift), o por un pipeline de reentrenamiento regular cada semana (aproximadamente) para el desfase conceptual (concept drift). Ambas opciones se consideran en este pipeline. En general, esta pequeña emulación autoalojada del diseño del sistema para MLOps se basa en las recomendaciones de mejores prácticas de Google MLOps https://cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning

## Diagrama de flujo del sistema ## 
![image](https://github.com/Alaboy19/model-retrain-gitops-fastapi/assets/47283347/fbc5aae8-3b17-41d4-bf90-74007c32dc69)

## Algunos puntos clave considerados ##

### MLflow ###
- Proporciona registro de experimentos
- Acceso general a artefactos de modelos para científicos de datos
- Reproducibilidad y control de versiones de modelos
- Evaluación y comparación de modelos basados en métricas
- Asignación de alias para modelos listos para diferentes entornos, como dev o prod
  
### FastAPI ###
- Protocolo ligero, simple y rápido que funciona de manera asíncrona con el servidor ASGI Uvicorn
- Compatible con pistas de tipo (type hints) en Python
- Integrado con Pydantic para la validación conveniente de tipos de datos
- Integrado con OpenAPI, generando automáticamente la documentación de la API y la interfaz de Swagger de forma nativa en la ruta /docs
  
### CI-CD ###
- Dado que es un servicio en línea, existe la necesidad de un empaquetado y despliegue rápidos del servicio a prod; por lo tanto, CI-CD es una mejor opción que los orquestadores como Ariflow, Prefect
- Cualquier push o pull request debe ser probado antes de enviarse a producción; CI-CD es una mejor opción también en este caso
- Los orquestadores podrían usarse posteriormente para preparar los datos para el feature store, como una abstracción de la ingeniería de datos
  
### render ###
- Forma gratuita de máquinas virtuales que permite desplegar servicios desde una imagen de registro de Docker

## Pasos realizados para desarrollar el pipeline ##
1. Reproduce el despliegue de ML en render con servicio de fastapi aquí https://github.com/Alaboy19/model-serving-github-actions-render, ya que es uno de los bloques fundamentales de este pipeline.
2. Aloja el registro de mlflow en algún lugar; en este caso, se aloja en GCP siguiendo el [tutorial](https://medium.com/@andrevargas22/how-to-launch-an-mlflow-server-with-continuous-deployment-on-gcp-in-minutes-7d3a29feff88).
3. Se agregó la ruta /trigger al servicio web, la cual desencadenará el flujo de trabajo de gitub actions externamente, mediante la API de github.
4. La ruta /reload-model que obtiene el último modelo asignado con el alias @prod en mlflow
5. El script train.py que obtiene new_data de una fuente estática y verifica si hay data drift; de ser así, inicia el entrenamiento y envía el nuevo modelo con el alias @prod al registro de mlflow
6. El archivo retrain.ci-cd.yaml que ejecuta todos los pasos para el reentrenamiento
## Pasos para reproducir el código ## 
1. Activa un entorno virtual y instala las dependencias con ``` pip install -q -r requriements.txt
``` O bien, puedes instalar poetry y ejecutar ```poetry install```
2. Genera un token para acceder a tu cuenta de dockerhub 
3. En los secretos de github actions → agrega secretos del repositorio para DATA_URL, HOT_RELOAD_URL(ruta a /reload-model)
4. También, genera REPO_TOKEN como acceso a tu repositorio y agrégalo a las variables del repositorio en la acción; es necesario para autenticarse en tu repositorio al solicitar el desencadenamiento de retrain.yml externamente desde el servicio de fasdtapi en render
5. También, agrega MLFLOW_TRACKING_URI obtenido desde GCP a las variables del repositorio 
6. Sigue las instrucciones en los archivos .github.workflows.ci-cd.yml y retrain.yml
7. Si se necesita un reentrenamiento y redesiñplego programado, descomenta la programación cron en .github/workflows/retrain.yml

## Mejores prácticas maduras de MLOps como referencia ## 
![image](https://github.com/Alaboy19/model-retraining-gitops-fastapi/assets/47283347/64412c18-9fd3-47d0-b724-07b9f5d889be)

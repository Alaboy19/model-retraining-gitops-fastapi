FROM --platform=linux/amd64 python:3.10-buster

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY *.py .

CMD ["python", "app_model.py"]
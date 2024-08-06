# Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install requirements.txt

COPY . /app

EXPOSE 8501

CMD ["streamlit", "run", "app.py"]

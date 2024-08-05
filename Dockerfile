# Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirement.txt /app/requirement.txt
RUN pip install --no-cache-dir -r /app/requirement.txt

COPY . /app

EXPOSE 8501

CMD ["streamlit", "run", "app.py"]
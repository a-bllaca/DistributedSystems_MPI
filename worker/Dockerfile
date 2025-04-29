
FROM python:3.9-slim

WORKDIR /app

COPY . /app

RUN pip install pandas redis

ENV PYTHONUNBUFFERED=1
CMD ["python", "worker.py"]
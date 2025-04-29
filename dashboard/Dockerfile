FROM python:3.9-slim

WORKDIR /app

COPY . /app

RUN pip install flask redis pandas

ENV FLASK_ENV=development
ENV PYTHONUNBUFFERED=1

CMD ["python", "app.py"]

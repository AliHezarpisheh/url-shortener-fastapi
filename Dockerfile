FROM python:3.13-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .

RUN apt-get update \
    && pip install --timeout 1000 --retries 5 --upgrade pip \
    && pip install --no-cache-dir --timeout 100 --retries 5 -r requirements-production.txt

COPY . .

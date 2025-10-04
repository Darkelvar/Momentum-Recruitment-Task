FROM python:3.13-slim

WORKDIR /code

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    postgresql-client \
    wget \
    && wget https://github.com/jwilder/dockerize/releases/download/v0.9.6/dockerize-alpine-linux-amd64-v0.9.6.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-alpine-linux-amd64-v0.9.6.tar.gz \
    && rm dockerize-alpine-linux-amd64-v0.9.6.tar.gz \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /code/
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . /code
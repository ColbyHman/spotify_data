FROM python:3.8-slim-buster

WORKDIR /app

COPY .. .

RUN python3 -m venv .venv

RUN .venv/bin/pip install requirements.txt

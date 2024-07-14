FROM python:3.11-slim

WORKDIR /opt/etl

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt requirements.txt

RUN  pip install --upgrade pip \
    && pip install -r requirements.txt

COPY . .

ENTRYPOINT ["python", "./main.py"]

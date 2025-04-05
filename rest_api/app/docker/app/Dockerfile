FROM python:3.12

WORKDIR /django_test

RUN apt update && apt -qy upgrade

COPY ../../requirements.txt django_test/requirements.txt

RUN pip install -r django_test/requirements.txt

COPY ../.. /django_test/

WORKDIR /django_test/
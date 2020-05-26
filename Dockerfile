FROM python:3.8-alpine

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
RUN pip install psycopg2

RUN mkdir /app
WORKDIR /app
COPY . /app

RUN adduser -D user
USER user
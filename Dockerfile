FROM python:3.11-alpine3.18

COPY requirements.txt /temp/requirements.txt
COPY jteam /jteam
WORKDIR /jteam
EXPOSE 8000

RUN apk update && \
    apk add --no-cache postgresql-libs gcc musl-dev && \
    pip install -r /temp/requirements.txt && \
    adduser --disabled-password jteam-user

USER jteam-user

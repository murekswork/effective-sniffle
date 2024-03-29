FROM python:3.10.4-slim-bullseye

ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

WORKDIR /code

COPY ./requirements.txt .
RUN apt-get update
RUN apt-get -y install libgdal-dev
RUN apt-get update
RUN apt-get -y install g++
RUN pip install -r requirements.txt

COPY . .

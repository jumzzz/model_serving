FROM python:3.8.12-slim

# set work directory
WORKDIR /usr/src/app/project
# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN apt-get update -y
RUN apt-get install libgomp1 -y

RUN pip install --upgrade pip
COPY requirements.txt /usr/src/app/project/requirements.txt
RUN pip install -r requirements.txt

# copy project
COPY tests /usr/src/app/tests
COPY project /usr/src/app/project/


FROM python:3.10-slim-buster

# set work directory
WORKDIR /src

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y curl

# install dependencies
COPY ./requirements /requirements
RUN pip install -U pip
RUN pip install -r /requirements/base.txt

COPY ./compose/local/backend/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

# copy project
COPY . .

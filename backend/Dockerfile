# pull official base image
FROM python:3.10.5

# set working directory
WORKDIR /usr/src/notifications/

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/notifications/
RUN pip install -r requirements.txt

# copy project
COPY . /usr/src/notifications/

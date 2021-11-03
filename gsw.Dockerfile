FROM ubuntu:20.04

WORKDIR /
ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get upgrade -y
RUN apt-get update && apt-get install -y \
  at \
  build-essential \
  wget \
  curl \
  git \
  libpq-dev \
  libffi-dev

# install python
RUN apt-get update && apt-get install -y \
  python3-pip \
  python3-dev \
  python3-venv
WORKDIR /usr/local/bin
RUN ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip

# copy our repo to the image
WORKDIR /home/ex2_ground_station_website
COPY . .
RUN pip3 install -r requirements.txt

# install node.js & npm
WORKDIR /home
RUN apt-get update && apt-get install -y \
  nodejs \
  npm

# Starts with a bash shell in the container
WORKDIR /home/ex2_ground_station_website
EXPOSE 5000
CMD /bin/bash

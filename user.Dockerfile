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
  libffi-dev \
  libzmq3-dev \
  libsocketcan-dev \
  pkg-config \
  gcc-multilib \
  g++-multilib \
  postgresql

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

# Install python dependencies
RUN pip3 install -r requirements.txt

# build libcsp
WORKDIR /home/ex2_ground_station_website
RUN ./build_libcsp.sh

# install node.js & npm
WORKDIR /home
RUN apt-get update && apt-get install -y \
  nodejs \
  npm

# set up environment
WORKDIR /home/ex2_ground_station_website
ENV FLASK_APP=groundstation/__init__.py
ENV FLASK_ENV=production
ENV APP_SETTINGS=groundstation.config.ProductionConfig
ENV SECRET_KEY="overwritten-in-keys-sh"
ENV SLACK_TOKEN="overwritten-in-keys-sh"
ENV LD_LIBRARY_PATH=libcsp/build
ENV PYTHONPATH=libcsp/build

ENTRYPOINT [ "./entrypoint.prod.sh" ]

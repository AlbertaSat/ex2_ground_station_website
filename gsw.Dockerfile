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

# set up environment
WORKDIR /home/ex2_ground_station_website
ENV FLASK_APP=groundstation/__init__.py
ENV FLASK_ENV=development
ENV APP_SETTINGS=groundstation.config.DevelopmentConfig
ENV SECRET_KEY="\xffY\x8dG\xfbu\x96S\x86\xdfu\x98\xe8S\x9f\x0e\xc6\xde\xb6$\xab:\x9d\x8b"
SHELL ["/bin/bash", "-c"]
RUN source ./update.sh

ENTRYPOINT [ "flask", "run", "--host=0.0.0.0", "--port=8000" ]

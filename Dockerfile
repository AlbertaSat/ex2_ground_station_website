FROM ubuntu:latest

WORKDIR /
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update
RUN apt-get install build-essential -y
RUN apt-get install wget curl -y
RUN apt-get install gcc-multilib g++-multilib -y
RUN apt-get install git -y
RUN apt-get install libsocketcan-dev -y
# postgres pip dependencies:
RUN apt-get install libpq-dev python3-dev -y

# install python
RUN apt-get update \
  && apt-get install -y python3-pip python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip

WORKDIR /home/ex2_ground_station_website
COPY . .
RUN pip3 install -r requirements.txt
# set Flask environment variables
ARG FLASK_APP
ARG FLASK_ENV
ARG APP_SETTINGS
ARG SECRET_KEY
ENV FLASK_APP=$FLASK_APP
ENV FLASK_ENV=$FLASK_ENV
ENV APP_SETTINGS=$APP_SETTINGS
ENV SECRET_KEY=$SECRET_KEY
# recreate the database (optional, probably should be an ARG)
RUN python3 manage.py recreate_db
RUN python3 manage.py seed_db
# install node.js & npm
RUN curl -sL https://deb.nodesource.com/setup_12.x | bash -
RUN apt-get install -y nodejs
WORKDIR /home/ex2_ground_station_website/groundstation/static
RUN npm install
RUN npm run build

EXPOSE 5000
WORKDIR /home/ex2_ground_station_website
CMD flask run

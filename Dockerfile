FROM ubuntu:latest

WORKDIR /
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update
RUN apt-get install build-essential -y
RUN apt-get install wget curl -y
RUN apt-get install git -y
# Flask PostgreSQL pip dependencies:
RUN apt-get install libpq-dev python3-dev -y
# libcsp dependencies:
RUN apt-get install gcc-multilib g++-multilib -y
RUN apt-get install libsocketcan-dev -y

# install python
RUN apt-get update \
  && apt-get install -y python3-pip python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip

# install zmq
RUN wget https://github.com/zeromq/libzmq/releases/download/v4.2.2/zeromq-4.2.2.tar.gz
RUN tar xvzf zeromq-4.2.2.tar.gz
RUN apt-get install -y libtool pkg-config build-essential autoconf automake uuid-dev
WORKDIR /zeromq-4.2.2
RUN ./autogen.sh
RUN ./configure
RUN make && make install
RUN apt-get install libzmq5 -y

# install libcsp
WORKDIR /home/
RUN git clone https://github.com/libcsp/libcsp.git
WORKDIR /home/libcsp/
RUN python3 waf configure --with-os=posix --enable-can-socketcan --enable-rdp --enable-hmac --enable-xtea --with-loglevel=debug --enable-debug-timestamp --enable-python3-bindings --with-driver-usart=linux --enable-if-zmqhub --enable-examples
RUN python3 waf build

# install node.js & npm
RUN curl -sL https://deb.nodesource.com/setup_12.x | bash -
RUN apt-get install -y nodejs

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
# create and seed the database
# RUN python3 manage.py recreate_db
# RUN python3 manage.py seed_db
# build the React frontend
WORKDIR /home/ex2_ground_station_website/groundstation/static
RUN npm install
RUN npm run build

WORKDIR /home/ex2_ground_station_website
EXPOSE 5000
# Starts with a bash shell in the container
CMD /bin/bash
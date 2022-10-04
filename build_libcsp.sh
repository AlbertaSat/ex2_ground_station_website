#!/bin/sh
# For Ubuntu

# Fetch submodules
git submodule update --init --recursive

# Fetch libcsp dependencies
apt update
apt install at \
    build-essential \
    wget \
    curl \
    libpq-dev \
    libzmq3-dev \
    libsocketcan-dev \
    pkg-config \
    gcc-multilib \
    g++-multilib \
    python3-dev \
    python3-pip -y

pip3 install numpy zmq pyserial

# Configure libcsp
# (Configuration flags taken from ex2_ground_station_software)
cd libcsp
git clone --branch master https://github.com/AlbertaSat/ex2_sdr.git
python3 waf configure --with-os=posix --enable-SDR --SDR-use-gnuradio --enable-rdp --enable-crc32 --enable-hmac --enable-xtea --with-loglevel=debug --enable-debug-timestamp --enable-python3-bindings --with-driver-usart=linux --enable-examples --enable-can-socketcan --enable-if-zmqhub
python3 waf build
cd ..

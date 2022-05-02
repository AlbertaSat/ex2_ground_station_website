#!/bin/sh
# For Ubuntu

# Fetch submodules
git submodule update --init --recursive

# Fetch libcsp dependencies
sudo apt update
sudo apt install at \
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

# Configure libcsp
# (Configuration flags taken from ex2_ground_station_software)
cd libcsp
python3 waf configure --with-os=posix --enable-can-socketcan --enable-rdp --enable-crc32 --enable-hmac --enable-xtea --with-loglevel=debug --enable-debug-timestamp --enable-python3-bindings --with-driver-usart=linux --enable-if-zmqhub --enable-examples
python3 waf build
cd ..
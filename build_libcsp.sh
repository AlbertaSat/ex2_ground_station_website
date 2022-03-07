#!/bin/sh
# For Ubuntu

# Fetch submodules
git submodule update --init --recursive

# Fetch libcsp dependencies
# NOTE: Python is required but not installed here as to not interfere
# with the setup-python Github Action
sudo apt install at \
    build-essential \
    wget \
    curl \
    libpq-dev \
    libzmq3-dev \
    libsocketcan-dev \
    pkg-config \
    gcc-multilib \
    g++-multilib -y

# Configure libcsp
cd libcsp
python3 waf configure --with-os=posix --enable-can-socketcan --enable-rdp --enable-crc32 --enable-hmac --enable-xtea --with-loglevel=debug --enable-debug-timestamp --enable-python3-bindings --with-driver-usart=linux --enable-if-zmqhub --enable-examples
python3 waf build
cd ..

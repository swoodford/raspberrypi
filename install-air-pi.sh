#!/bin/bash
# This script will install the Shairport Airplay emulator for Raspberry Pi

# Install deps
sudo apt-get install -y git libao-dev libssl-dev libcrypt-openssl-rsa-perl libio-socket-inet6-perl libwww-perl avahi-utils libmodule-build-perl

# Install perl net sdp
git clone https://github.com/njh/perl-net-sdp.git perl-net-sdp
cd perl-net-sdp
perl Build.PL
sudo ./Build
sudo ./Build test
sudo ./Build install
cd ~

# Install shairport
git clone https://github.com/hendrikw82/shairport.git
cd shairport
make

# Start up Airplay
./shairport.pl -a AirPi &

echo "Airplay started as device: AirPi"
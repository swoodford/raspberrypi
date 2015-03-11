#!/bin/bash
# This script installs Twython on Raspberry Pi
# https://github.com/ryanmcgrath/twython

sudo apt-get update
sudo apt-get upgrade
sudo apt-get install python-setuptools -y
sudo easy_install pip
sudo pip install twython

echo "Twython Installed."
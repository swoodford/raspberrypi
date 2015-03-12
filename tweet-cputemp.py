#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This script will tweet your current Raspberry Pi CPU temperature, date, time and ip-geolocation
# Requires Twython, API credentials set as env vars

import sys
import os
import time
from twython import Twython

# Set Credentials from environment variables
CONSUMER_KEY = os.getenv("CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("CONSUMER_SECRET")
ACCESS_KEY = os.getenv("ACCESS_KEY")
ACCESS_SECRET = os.getenv("ACCESS_SECRET")

api = Twython(CONSUMER_KEY,CONSUMER_SECRET,ACCESS_KEY,ACCESS_SECRET) 

cmd = 'awk \'{printf("%.1f °F\\n",$1*1.8/1e3)}\' /sys/class/thermal/thermal_zone0/temp'
temp = os.popen(cmd).readline()
cmd2 = 'date'
time = os.popen(cmd2).readline()

# Get geolocation using IP address
getlat = 'curl -s http://whatismycountry.com/ | sed -n \'s/.*Coordinates \\(.*\\)<.*/\\1/p\' | cut -d \' \' -f1'
getlong = 'curl -s http://whatismycountry.com/ | sed -n \'s/.*Coordinates \\(.*\\)<.*/\\1/p\' | cut -d \' \' -f2'

lat = os.popen(getlat).readline()
long = os.popen(getlong).readline()

lat = lat.strip()
long = long.strip()

# Tweet with CPU temp, date, time and ip-geolocation
api.update_status(status='My current #RaspberryPi CPU temperature is '+temp+' on '+time+'', lat=(lat), long=(long))
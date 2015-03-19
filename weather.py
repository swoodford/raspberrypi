#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This script will tweet current NYC weather conditions and IP-geolocation
# Requires Twython, API credentials set as env vars, seperate getweather.sh script

import sys
import os
from twython import Twython

# Set Credentials from environment variables
CONSUMER_KEY = os.getenv("CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("CONSUMER_SECRET")
ACCESS_KEY = os.getenv("ACCESS_KEY")
ACCESS_SECRET = os.getenv("ACCESS_SECRET")

api = Twython(CONSUMER_KEY,CONSUMER_SECRET,ACCESS_KEY,ACCESS_SECRET) 

cmd = 'bash getweather.sh'
weather = os.popen(cmd).readline()

# Get geolocation using IP address
getlat = 'curl -s http://whatismycountry.com/ | sed -n \'s/.*Coordinates \\(.*\\)<.*/\\1/p\' | cut -d \' \' -f1'
getlong = 'curl -s http://whatismycountry.com/ | sed -n \'s/.*Coordinates \\(.*\\)<.*/\\1/p\' | cut -d \' \' -f2'

lat = os.popen(getlat).readline()
long = os.popen(getlong).readline()

lat = lat.strip()
long = long.strip()

# Tweet weather and IP-geolocation
api.update_status(status='#NYC #weather '+weather+'', lat=(lat), long=(long))

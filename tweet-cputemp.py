#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This script will tweet your current Raspberry Pi CPU temperature
# Requires Twython, API credentials set as env vars

import sys, os, time
from twython import Twython

CONSUMER_KEY = os.getenv("CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("CONSUMER_SECRET")
ACCESS_KEY = os.getenv("ACCESS_KEY")
ACCESS_SECRET = os.getenv("ACCESS_SECRET")

api = Twython(CONSUMER_KEY,CONSUMER_SECRET,ACCESS_KEY,ACCESS_SECRET) 

cmd = 'awk \'{printf("%.1f °F\\n",$1*1.8/1e3)}\' /sys/class/thermal/thermal_zone0/temp'
temp = os.popen(cmd).readline()
cmd2 = 'date'
time = os.popen(cmd2).readline()
# api.update_status(status='My current #RaspberryPi CPU temperature is '+temp+' on '+time.strftime("%c"))
api.update_status(status='My current #RaspberryPi CPU temperature is '+temp+' on '+time+'')
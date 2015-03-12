#!/usr/bin/env python

# This script will tweet an image from the RPi webcam along with the current date and time
# Requires Twython, API credentials set as env vars

import pygame
import pygame.camera
import sys
import os
import time
from pygame.locals import *
from twython import Twython

# Set Credentials from environment variables
CONSUMER_KEY = os.getenv("CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("CONSUMER_SECRET")
ACCESS_KEY = os.getenv("ACCESS_KEY")
ACCESS_SECRET = os.getenv("ACCESS_SECRET")

api = Twython(CONSUMER_KEY,CONSUMER_SECRET,ACCESS_KEY,ACCESS_SECRET) 

# Take a photo from the camera
pygame.init()
pygame.camera.init()
cam = pygame.camera.Camera("/dev/video0",(1024,768))
cam.start()
image = cam.get_image()
pygame.image.save(image,'webcam.jpg')
photo = open('webcam.jpg','rb')

# Get geolocation using IP address
getlat = 'curl -s http://whatismycountry.com/ | sed -n \'s/.*Coordinates \\(.*\\)<.*/\\1/p\' | cut -d \' \' -f1'
getlong = 'curl -s http://whatismycountry.com/ | sed -n \'s/.*Coordinates \\(.*\\)<.*/\\1/p\' | cut -d \' \' -f2'

lat = os.popen(getlat).readline()
long = os.popen(getlong).readline()

lat = lat.strip()
long = long.strip()

# Tweet with photo and geolocation
api.update_status_with_media(media=photo, status='#RaspberryPi #RaspberryPiCam #Twython ' + time.strftime("%c"), lat=(lat), long=(long))
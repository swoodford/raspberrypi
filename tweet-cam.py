#!/usr/bin/env python

# This script will tweet an image from the RPi webcam along with the current date and time
# Requires Twython, API credentials set as env vars

import time, pygame, pygame.camera, sys, os
from pygame.locals import *
from twython import Twython

CONSUMER_KEY = os.getenv("CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("CONSUMER_SECRET")
ACCESS_KEY = os.getenv("ACCESS_KEY")
ACCESS_SECRET = os.getenv("ACCESS_SECRET")

api = Twython(CONSUMER_KEY,CONSUMER_SECRET,ACCESS_KEY,ACCESS_SECRET) 

pygame.init()
pygame.camera.init()
cam = pygame.camera.Camera("/dev/video0",(1024,768))
cam.start()
image = cam.get_image()
pygame.image.save(image,'webcam.jpg')

photo = open('webcam.jpg','rb')
api.update_status_with_media(media=photo, status='#RaspberryPiCam ' + time.strftime("%c"))

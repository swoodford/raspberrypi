#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Raspberry Pi and MAX7219 LED Board Stock Symbol Price Monitor
# A simple stock ticker price change monitor of today's positive or negative change using a MAX7219 LED Board


import re
import time
import argparse
import atexit
import sys
import os

import decimal
import errno
import signal
import urllib2
# import ystockquote
import json
import requests

from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.virtual import viewport
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT

from socket import error as SocketError

debug = 0

# Stock quote configuration:
tickerSymbol = 'AAPL'

# MAX7219 configuration:
serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial, cascaded=4, block_orientation=-90, rotate=0)

# Turn off all the LEDs
def lightsOut():
    device.cleanup()

# Run lightsOut at exit
atexit.register(lightsOut)

# Console message and LEDs off while market closed
def marketClosed():
  print "Stock Market Closed.", now
  lightsOut()
  time.sleep(60)

# Debugging
if debug == 1:
  allInfo = ystockquote.get_all(tickerSymbol)
  print allInfo

decimal.getcontext().prec = 8

# Handle timeouts gracefully
def timeoutHandler(signum, frame):
  print "Error: Timeout fetching quote."
  lightsOut()
  time.sleep(10)
  signal.alarm(0)
  return

signal.signal(signal.SIGALRM, timeoutHandler)

# Scroll message across the LCD Panel
# msg = "This is a test! 123456789 ABCDEFG"


# # Main program logic follows:
# if __name__ == '__main__':

#   try:
#       while True:
#       	print(msg)
#       	show_message(device, msg, fill="white", font=proportional(LCD_FONT))

# Main function to get the quote and animate the LEDs
def getQuote(change):
  if debug == 1:
    print "Function getQuote"

  try:
    signal.alarm(10)
    rsp = requests.get('https://finance.google.com/finance?q=' + tickerSymbol + '&output=json')
    if rsp.status_code in (200,):
      fin_data = json.loads(rsp.content[6:-2].decode('unicode_escape'))
      print('Change: {}'.format(fin_data['c']))
      change = format(fin_data['c'])
  except urllib2.HTTPError as err:
    if err.code == 404:
      print "Error: 404 Not Found."
    else:
      print "Error: ", err.code
  except urllib2.URLError as err:
    print "Error: Connection reset by peer."
  except SocketError as err:
    if err.errno == errno.ECONNRESET:
      print "Error: Connection reset by peer."
  # price = ystockquote.get_price(tickerSymbol)

  # while change == 'N/A':
  #   print "Error: No price change data."
  #   time.sleep(60)
  #   change = ystockquote.get_change(tickerSymbol)

  # changedecimal = decimal.Decimal(change)
  # pricedecimal = Decimal(price)
  # changedecimal = 0

  # Reset timeout
  signal.alarm(0)

  # Console message with price change
  print "$ Change: ", change
  # print pricedecimal

  # lastclose = Decimal(pricedecimal) - Decimal(changedecimal)

  # print lastclose

  show_message(device, (str (change)), fill="white", font=proportional(LCD_FONT))
  time.sleep(1)
  # sense.show_message(str (changedecimal), text_colour=[LED_BRIGHTNESS, 0, 0])

# Main program logic follows:
if __name__ == '__main__':

  try:
    while True:
      now = datetime.datetime.now()
      # print now

      # Between Monday - Friday
      if 0 <= now.weekday() <= 5:
        if debug == 1:
          print "Weekday: ", now.weekday()
        # print now.hour

        # Between 9AM - 5PM
        if now.hour == 9:
          if debug == 1:
            print "Hour 9AM"
          if now.minute >= 30:
            if debug == 1:
              print "Minute 30 or later"
            if 9 <= now.hour <= 17:
              # print "Hour: ", now.hour
              # print now.time()

              if debug == 1:
                print "Calling function getQuote"

              getQuote(0)

          else:
            marketClosed()

        else:
          if 9 <= now.hour <= 15:
            if debug == 1:
              print "Hour between 10AM-4PM"
            # print "Hour: ", now.hour
            # print now.time()

            if debug == 1:
              print "Calling function getQuote"

            getQuote(0)

          else:
            marketClosed()

      else:
        marketClosed()

  # Handle Ctrl-C gracefully
  except KeyboardInterrupt:
      print ' - Exiting'
      lightsOut()
      try:
          sys.exit(0)
      except SystemExit:
          os._exit(0)

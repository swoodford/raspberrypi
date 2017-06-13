#!/usr/bin/python

# Raspberry Pi and Sense Hat Stock Symbol Price Ticker
# A simple stock ticker price change monitor of today's positive or negative change using the Sense Hat
# Shows a red/green solid color 8x8 matrix up/down arrow and stock price ticker

import datetime
import time
import ystockquote
import atexit
import sys
import os
import urllib2

from socket import error as SocketError
import errno

from decimal import *

from sense_hat import SenseHat

sense = SenseHat()

# Rotation (Default=0)
sense.set_rotation(90)

debug = 0

# Stock quote configuration:
tickerSymbol = 'AAPL'


# Define functions which animate LEDs in various ways.

def lightsOut():
	# Turn off all the LEDs.
	if debug == 1:
		print ('Turning off all LEDs.')
	sense.clear()

def marketClosed():
	print "Stock Market Closed.", now
	lightsOut()
	time.sleep(60)

atexit.register(lightsOut)

if debug == 1:
	allInfo = ystockquote.get_all(tickerSymbol)
	print allInfo
# 	quote = ystockquote.get_change(tickerSymbol)
# 	print quote

# print tickerSymbol + " Price = " + allInfo["price"]
# print tickerSymbol + " Change = " + allInfo["change"]
# print allInfo["change"]

# print allInfo

getcontext().prec = 8

def getQuote(change):
	if debug == 1:
		print "Function getQuote"

	try:
		change = ystockquote.get_change(tickerSymbol)
	except urllib2.HTTPError as err:
		if err.code == 404:
			print "404 ERROR"
		else:
			print "err.code: ", err.code
			# pass
	except urllib2.URLError as err:
		print "Connection reset by peer: ", err.code
		# pass
	except SocketError as err:
	    if err.errno == errno.ECONNRESET:
	        print "Connection reset by peer."
	    	pass
	# price = ystockquote.get_price(tickerSymbol)

	while change == 'N/A':
		print "ERROR: NO PRICE CHANGE DATA!"
		time.sleep(60)
		change = ystockquote.get_change(tickerSymbol)

	changedecimal = Decimal(change)
	# pricedecimal = Decimal(price)
	# changedecimal = 0
	print "$ Change: ", changedecimal
	# print pricedecimal

	# lastclose = Decimal(pricedecimal) - Decimal(changedecimal)

	# print lastclose

	# Negative
	if changedecimal < 0:
		LED_BRIGHTNESS = abs(int(round(100 * changedecimal)))
		if LED_BRIGHTNESS > 255:
			LED_BRIGHTNESS = 255
		if LED_BRIGHTNESS < 50:
			LED_BRIGHTNESS = 50
		if debug == 1:
			print "Brightness: ", LED_BRIGHTNESS
		R = [LED_BRIGHTNESS, 0, 0] # Red
		G = [0, LED_BRIGHTNESS, 0]  # Green
		B = [0, 0, 0]  # Black
		
		down_arrow = [
		R, R, R, R, R, R, R, R,
		R, R, R, R, R, R, R, R,
		B, R, R, R, R, R, R, B,
		B, R, R, R, R, R, R, B,
		B, B, R, R, R, R, B, B,
		B, B, R, R, R, R, B, B,
		B, B, B, R, R, B, B, B,
		B, B, B, R, R, B, B, B
		]

		sense.set_pixels(down_arrow)
		time.sleep(1.5)
		sense.show_message(str (changedecimal), text_colour=[LED_BRIGHTNESS, 0, 0])

	# Positive
	if changedecimal > 0:
		LED_BRIGHTNESS = int(round(100 * changedecimal))
		if LED_BRIGHTNESS > 255:
			LED_BRIGHTNESS = 255
		if LED_BRIGHTNESS < 50:
			LED_BRIGHTNESS = 50
		if debug == 1:
			print "Brightness: ", LED_BRIGHTNESS
		R = [LED_BRIGHTNESS, 0, 0] # Red
		G = [0, LED_BRIGHTNESS, 0]  # Green
		B = [0, 0, 0]  # Black
		
		up_arrow = [
		B, B, B, G, G, B, B, B,
		B, B, B, G, G, B, B, B,
		B, B, G, G, G, G, B, B,
		B, B, G, G, G, G, B, B,
		B, G, G, G, G, G, G, B,
		B, G, G, G, G, G, G, B,
		G, G, G, G, G, G, G, G,
		G, G, G, G, G, G, G, G
		]

		sense.set_pixels(up_arrow)
		time.sleep(1.5)
		sense.show_message( str (changedecimal), text_colour=[0, LED_BRIGHTNESS, 0])

	# Zero
	if changedecimal == 0:
		if debug == 1:
			print "Zero Change!"
		# sense.clear([50, 50, 50])
		sense.show_message(str (changedecimal), text_colour=[50, 50, 50])

	time.sleep(.5)

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

	except KeyboardInterrupt:
		lightsOut()
		print ' - Exiting'
		try:
			sys.exit(0)
		except SystemExit:
			os._exit(0)

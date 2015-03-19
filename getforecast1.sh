#!/bin/bash
# Get current NYC weather forecast and abbreviate as much as possible for Twitter
# Requires weather-util

# Set your location by city or airport code
LOCATION=nyc

# Get weather conditions, in imperial units, without preamble or indentation
weather $LOCATION --imperial -q -f | tail -n 25 | head -n 7 | \
# Remove new line breaks
sed ':a;N;$!ba;s/\n/ /g' | \
# Replace three periods with a space
sed -r 's#\.{3}#\ #g' | \
# Remove multiple spaces
sed -r 's/(\s?\.)//g' | \
# Abbreviations
sed s#IN\ EFFECT\ ##g | \
sed s#Temperature#Temp#g | \
sed s#degrees#deg.#g | \
sed s#Relative\ Humidity#Humid.#g | \
sed s#conditions#cond.#g | \
sed s#gusting#gusts#g | \
sed s#Windchill#Windch.#g | \
sed s#SUNDAY#SUN.#g | \
sed s#MONDAY#MON.#g | \
sed s#TUESDAY#TUES.#g | \
sed s#WEDNESDAY#WED.#g | \
sed s#THURSDAY#THURS.#g | \
sed s#FRIDAY#FRI.#g | \
sed s#SATURDAY#SAT.#g | \
sed s#IN\ THE\ ##g | \
sed s#THEN\ BECOMING\ ##g | \
sed s#NORTHWEST#NW#g | \
sed s#NORTHEAST#NE#g | \
sed s#SOUTHWEST#SW#g | \
sed s#SOUTHEAST#SE#g | \
# Limit to first 140 characters - 24 for hashtags
cut -c 2-117

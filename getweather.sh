#!/bin/bash
# Get current NYC weather and abbreviate as much as possible for Twitter
# Requires weather-util

# Set your location by city or airport code
LOCATION=nyc

# Get weather conditions, in imperial units, without preamble or indentation
weather $LOCATION --imperial -q | \
# Remove new line breaks
sed ':a;N;$!ba;s/\n/ /g' | \
# Abbreviations
sed s#Temperature#Temp#g | \
sed s#degrees#deg.#g | \
sed s#Relative\ Humidity#Humid.#g | \
sed s#conditions#cond.#g | \
sed s#gusting#gusts#g | \
sed s#Windchill#Windch.#g

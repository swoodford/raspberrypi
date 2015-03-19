#!/usr/bin/env python

# This script will tweet the text that is passed as an argument
# Requires Twython, API credentials set as env vars
# Usage: python tweet-status.py 'Hello Everyone, this is my Raspberry Pi tweeting you more nonsense'

import sys
import os
from twython import Twython

# Set Twitter Credentials from environment variables
CONSUMER_KEY = os.getenv("CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("CONSUMER_SECRET")
ACCESS_KEY = os.getenv("ACCESS_KEY")
ACCESS_SECRET = os.getenv("ACCESS_SECRET")

api = Twython(CONSUMER_KEY,CONSUMER_SECRET,ACCESS_KEY,ACCESS_SECRET) 

# Tweet
api.update_status(status=sys.argv[1][:140])

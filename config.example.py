#
# Copy this file to 'config.py' and then edit that
#

import logging

# Celery broker URL
# By default, this is Redis.
CELERY_BROKER_URL = 'redis://localhost:6379/0'

# Debug mode host and port.
DEBUG_HOST = "127.0.0.1"
DEBUG_PORT = 5000

# Disable pickle.
CELERY_ACCEPT_CONTENT = ['json', 'msgpack', 'yaml']

# Your all users API key here.
# This is used for both verification, and posting data to the server.
API_KEY = "yourkeyhere"

# Your username for the bot to work on.
API_USERNAME = "taciturn"

# The domain of the forum to work on.
API_FORUM = "http://www.example.com"

# Set logging level
LOG_LEVEL = logging.INFO

# Set language
LANGUAGE = "en"
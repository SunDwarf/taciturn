import logging

import celery
from flask import g, Flask

from taciturn.discourse_client import Client

logger = logging.getLogger("taciturn")


# Synchronous tasks.
def verify(request):
    """
    Verifies a request against the config.
    """
    assert isinstance(g.celery, celery.Celery)
    assert isinstance(g.app, Flask)
    assert isinstance(g.client, Client)

    if request is None:
        return False
    if len(request) < 1:
        return False
    if not isinstance(request[0], str):
        return False
    if request[0] != g.client.api_key:
        logger.error("Failed to validate API key! Key provided was: {}".format(request[0]))
        return False

@g.celery.task
def process(data):
    print("Entered processor")



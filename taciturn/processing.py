import logging
from flask import Flask

from app import app, celery, client

logger = logging.getLogger("taciturn")

from celery.utils.log import get_task_logger
task_logger = get_task_logger(__name__)


# Synchronous tasks.
def verify(request):
    """
    Verifies a request against the config.
    """
    if request is None:
        return False
    if len(request) < 1:
        return False
    if not isinstance(request[0], str):
        return False
    if request[0] != client.api_key:
        logger.error("Failed to validate API key! Key provided was: {}".format(request[0]))
        return False
    return True

# Async stuff

@celery.task
def process(data, ptype):
    task_logger.info("Entered processor, type {}".format(ptype))




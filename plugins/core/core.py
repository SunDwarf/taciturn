import logging

logger = logging.getLogger("taciturn-core")

def init(app, celery, client):
    logger.debug("Initializing core plugin...")
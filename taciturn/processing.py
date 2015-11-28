import logging
from celery import group

from app import app, celery, client
from taciturn import registry


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

    if data[2]["username"] == app.config["API_USERNAME"]:
        return

    if ptype == 0:
        g = group(func.s(data) for func in registry.topic_created_registry.values())
    elif ptype == 1:
        g = group(func.s(data) for func in registry.post_created_registry.values())
    else:
        task_logger.error("Unable to handle event of type {}".format(ptype))
        return

    # Call the group.
    g.apply_async()




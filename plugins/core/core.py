import logging
from core_plugin import username_ping
from taciturn import registry

logger = logging.getLogger("taciturn-core")

data = {
    "app": None,
    "celery": None,
    "client": None
}

def init(app, celery, client):
    logger.debug("Initializing core plugin...")
    data["app"] = app
    data["celery"] = celery
    data["client"] = client

    logger.debug("Creating post handler...")
    registry.post_handler("username_ping")(username_ping.username_ping)
    registry.nick_ping("version")(username_ping.version_ping)

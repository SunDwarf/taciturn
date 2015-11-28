from pprint import pprint, pformat

from celery import Celery
from flask import Blueprint, g
from flask import request

from . import processing

hooks_bp = Blueprint('hooks', "tacticum",
                    url_prefix="/hooks")

import logging
logger = logging.getLogger("tacitun")


@hooks_bp.route("/topic_created", methods=["POST"])
def topic_created():
    logger.debug("Received new topic created hook, processing...")
    logger.debug("JSON Data: \n" + pformat(request.get_json()))

    valid = processing.verify(request.get_json())

    if not valid:
        return "NO", 200, {"Content-Type": "text/plain"}

    return "OK", 200, {"Content-Type": "text/plain"}

@hooks_bp.route("/post_created", methods=["POST"])
def post_created():
    logger.debug("Received new post created hook, processing...")
    logger.debug("JSON Data: \n" + pformat(request.get_json()))

    valid = processing.verify(request.get_json())

    if not valid:
        return "NO", 200, {"Content-Type": "text/plain"}

    # Create a new processing task.
    processing.process(request.get_json()[1:])

    return "OK", 200, {"Content-Type": "text/plain"}
from pprint import pformat

from flask import Blueprint
from flask import request

from taciturn import processing

hooks_bp = Blueprint('hooks', "taciturn",
                    url_prefix="/hooks")

import logging
logger = logging.getLogger("taciturn")


@hooks_bp.route("/topic_created", methods=["POST"])
def topic_created():
    logger.debug("Received new topic created hook, processing...")
    logger.debug("JSON Data: \n" + pformat(request.get_json()))

    valid = processing.verify(request.get_json())

    if not valid:
        return "NO", 400, {"Content-Type": "text/plain"}

    # Create a new processing task.
    processing.process.delay(request.get_json()[1:], 1)

    return "OK", 200, {"Content-Type": "text/plain"}

@hooks_bp.route("/post_created", methods=["POST"])
def post_created():
    logger.debug("Received new post created hook, processing...")
    logger.debug("JSON Data: \n" + pformat(request.get_json()))

    valid = processing.verify(request.get_json())

    if not valid:
        return "NO", 400, {"Content-Type": "text/plain"}

    # Create a new processing task.
    processing.process.delay(request.get_json()[1:], 1)

    return "OK", 200, {"Content-Type": "text/plain"}
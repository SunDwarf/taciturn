import logging
import traceback

import sys
from celery import Celery
from flask import Flask
from flask.ext.babel import Babel
import init

__version__ = (0, 1, 0)

app = Flask(__name__)

# --> Load config
app.config.from_object("config")

# --> Set version
app.config["TACITURN_VERSION"] = __version__

# --> Setup logging
formatter = logging.Formatter('%(asctime)s - [%(levelname)s] %(name)s - %(message)s')
root = logging.getLogger()

root.setLevel(app.config["LOG_LEVEL"])

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(formatter)
root.addHandler(consoleHandler)

logger = logging.getLogger("taciturn")

# --> Init Babel
babel = Babel(app)

@babel.localeselector
def get_locale():
    # Return the configured language.
    return app.config.get("LANGUAGE", "en")

logger.info("taciturn starting up...")

# --> Init celery

logger.info("Initializing celery connector...")

def make_celery(app):
    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery

celery = make_celery(app)

logger.info("Celery connector created...")

# --> Create client
logger.info("Creating client...")
from taciturn.discourse_client import Client
client = Client(host=app.config["API_FORUM"], api_key=app.config["API_KEY"], api_username=app.config["API_USERNAME"])

logger.info("Testing client connectivity...")

try:
    client.categories()
except Exception as e:
    traceback.print_exc()
    logger.error("Unable to connect - aborting.")
    sys.exit(1)

logger.info("Created client.")

# --> Init app
logger.info("Loading application...")
init.core_init(app)

logger.info("Loaded taciturn classes.")

# --> Init plugins
logger.info("Loading plugins...")
plugins = init.plugin_init(app, celery, client)

logger.info("Loaded plugins.")

# --> Done.
logger.info("tactiturn startup finished.")

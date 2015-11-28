import logging

from flask import Flask, g

__version__ = (0, 1, 0)

app = Flask(__name__)

# --> Load config
app.config.from_object("config")

# --> Set version
app.config["TACITURN_VERSION"] = __version__

# --> Init celery

from celery import Celery

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

# --> Blueprints
import taciturn
app.register_blueprint(taciturn.core_bp)
app.register_blueprint(taciturn.hooks_bp)

# --> Create client
from taciturn.discourse_client import Client
client = Client(host=app.config["API_FORUM"], api_key=app.config["API_KEY"], api_username=app.config["API_USERNAME"])

# --> Setup logging
formatter = logging.Formatter('%(asctime)s - [%(levelname)s] %(name)s - %(message)s')
root = logging.getLogger()

root.setLevel(app.config["LOG_LEVEL"])

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(formatter)
root.addHandler(consoleHandler)

# --> Set globals
@app.before_request
def before_request():
    g.app = app
    g.celery = celery
    g.client = client

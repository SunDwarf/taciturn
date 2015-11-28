from celery import __version__ as cver
from flask import Blueprint
from flask import __version__ as fver
from app import celery, app

from pprint import pformat

core_bp = Blueprint('core', "taciturn",
                    template_folder='templates')

@core_bp.route("/")
def root():
    # Get inspect instance
    i = celery.control.inspect()

    reg = i.registered()
    queue = i.active()

    fmt = """  _______ _____
 |__   __/ ____|
    | | | |
    | | | |
    | | | |____
    |_|  \_____|

Taciturn v{ver}{debug}.

Celery: v{cver}
Flask: v{fver}

Celery broker: {broker}
App: {app}

-----

Celery registered tasks:
{reg}

-----

Celery queue:
{queue}

All systems nominal.
""""".format(ver='.'.join(map(str, app.config["TACITURN_VERSION"])), broker=app.config["CELERY_BROKER_URL"],
    app=app, reg=pformat(reg), queue=pformat(queue), fver=fver, cver=cver,
    debug=" serving on {}:{}".format(
        app.config["DEBUG_HOST"], app.config["DEBUG_PORT"])
    if app.config["DEBUG"] else None)
    return fmt, 200, {"Content-Type": "text/plain"}
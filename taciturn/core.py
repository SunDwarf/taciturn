from celery import Celery
from celery import __version__ as cver
from flask import Blueprint, g
from flask import __version__ as fver

from pprint import pformat

core_bp = Blueprint('core', "tacticum",
                    template_folder='templates')

@core_bp.route("/")
def root():
    # Get inspect instance
    assert isinstance(g.celery, Celery)
    i = g.celery.control.inspect()

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
""""".format(ver='.'.join(map(str, g.app.config["TACITURN_VERSION"])), broker=g.app.config["CELERY_BROKER_URL"],
    app=g.app, reg=pformat(reg), queue=pformat(queue), fver=fver, cver=cver,
    debug=" serving on {}:{}".format(
        g.app.config["DEBUG_HOST"], g.app.config["DEBUG_PORT"])
    if g.app.config["DEBUG"] else None)
    return fmt, 200, {"Content-Type": "text/plain"}
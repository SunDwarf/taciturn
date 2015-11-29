import sys
from celery import __version__ as cver
from flask import Blueprint
from flask import __version__ as fver
from app import celery, app

from pprint import pformat

from taciturn import registry
from taciturn.locale import Locale


core_bp = Blueprint('core', "taciturn",
                    template_folder='templates')

@core_bp.route("/")
def root():
    from app import plugins

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

-----

Plugins:
{plug}

All systems nominal.
""""".format(ver='.'.join(map(str, app.config["TACITURN_VERSION"])), broker=app.config["CELERY_BROKER_URL"],
    app=app, reg=pformat(reg), queue=pformat(queue), fver=fver, cver=cver,
    debug=" serving on {}:{}".format(
        app.config["DEBUG_HOST"], app.config["DEBUG_PORT"])
    if app.config["DEBUG"] else None,
    plug='\n'.join([" - {0} (from {1})".format(name, value[1].path) for (name, value) in plugins.items()]))
    return fmt, 200, {"Content-Type": "text/plain"}

@core_bp.route("/info")
def info():
    if app.debug:
        cfg = app.config
    else:
        cfg = "N/A"
    fmt = """Path:
{path}

Config:
{cfg}

Locale database - Custom:
{loc1}
Locale database - Default:
{loc2}

Registry - Post Handlers:
{ph}

Registry - Topic Handlers:
{th}

Registry - Nickping Handlers:
{np}
""".format(path=pformat(sys.path), cfg=pformat(cfg), ph=pformat(registry.post_created_registry),
            th=pformat(registry.topic_created_registry), np=pformat(registry.nick_ping_registry),
            loc2=pformat(Locale.get().def_msgs), loc1=pformat(Locale.get().msgs))
    return fmt, 200, {"Content-Type": "text/plain"}
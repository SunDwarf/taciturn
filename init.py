import os
import sys
import traceback

import yaml
from flask import Flask
from celery import Celery
from taciturn.discourse_client import Client
import importlib

try:
    from os import scandir, walk
except ImportError:
    from scandir import scandir, walk

import logging
logger = logging.getLogger("taciturn")

def core_init(app):
    """
    Initializes Taciturn core.
    """
    import taciturn.hooks
    import taciturn.core
    app.register_blueprint(taciturn.core.core_bp)
    app.register_blueprint(taciturn.hooks.hooks_bp)


def plugin_init(app: Flask, celery: Celery, client: Client):
    """
    Initializes plugins.
    """
    # Search for plugins

    plugins = {}

    for dir in scandir(os.path.join(os.getcwd(), "plugins")):
        # Scan for files in that directory.
        logger.info("Searching plugin directory {}...".format(dir.name))
        valid = False
        for file in scandir(dir.path):
            if not file.is_dir() and file.name == "plugin.yml":
                with open(file.path) as f:
                    data = yaml.load(f)
                    name = data.get("name", dir.name)
                    if not "main_module" in data:
                        logger.error("No main module in plugin {}!".format(name))
                        break
                    else:
                        # Insert into the path, and attempt to import the module.
                        if dir.path not in sys.path:
                            sys.path.insert(0, dir.path)
                        try:
                            module = importlib.import_module(data["main_module"])
                        except:
                            logger.error("Plugin {} failed to load!".format(name))
                            traceback.print_exc()
                        plugins[name] = module
                        # Get init module name.
                        funname = data.get("init_function", "init")
                        if hasattr(module, funname):
                            # Call init.
                            try:
                                getattr(module, funname)(app, celery, client)
                            except:
                                logger.error("Plugin {} failed to load!".format(name))
                                traceback.print_exc()
                                break
                        valid = True
        if not valid:
            logger.error("Plugin in directory \"{}\" failed to load properly.".format(dir.name))

    return plugins


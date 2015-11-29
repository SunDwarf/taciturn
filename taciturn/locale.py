import os

import yaml
import sys

try:
    from os import scandir
except ImportError:
    from scandir import scandir

def merge_dicts(*dict_args):
    '''
    Given any number of dicts, shallow copy and merge into a new dict,
    precedence goes to key value pairs in latter dicts.
    '''
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result


class Locale(object):
    instance = None

    def __init__(self, language: str=None):
        self.lang = language
        self.def_msgs = {}
        self.msgs = {}

    @classmethod
    def get(cls, lang=None):
        if cls.instance is None:
            cls.instance = cls(lang)
        return cls.instance

    def load_all(self):
        # Search path
        for _ in sys.path:
            if not os.path.exists(_):
                continue
            for dir in scandir(_):
                if dir.name == "translations":
                    for file in scandir(dir.path):
                        # YAML load all messages files
                        if file.name == "msgs.yml":
                            with open(file.path) as f: data = yaml.load(f)
                            self.def_msgs = merge_dicts(self.def_msgs, data)
                        elif file.name == "msgs.{}.yml".format(self.lang):
                            with open(file.path) as f: data = yaml.load(f)
                            self.msgs = merge_dicts(self.msgs, data)

    def gettext(self, key):
        return self.msgs.get(key, self.def_msgs.get(key, key))


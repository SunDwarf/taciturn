import types


post_created_registry = {}
topic_created_registry = {}
nick_ping_registry = {}


def post_handler(hname):
    """
    Decorator for adding a new post handler.
    """

    def real_dec(func: types.FunctionType):
        if hname is None:
            name = func.__name__
        else:
            name = hname
        post_created_registry[name] = func
        return func
    return real_dec

def topic_handler(hname):
    """
    Decorator for adding a new topic handler.

    You probably won't need this.
    """

    def real_dec(func: types.FunctionType):
        if hname is None:
            name = func.__name__
        else:
            name = hname
        topic_created_registry[name] = func
        return func
    return real_dec

def nick_ping(hname):
    """
    Adds a handler for a nick ping command (@taciturn ping)
    """

    def real_dec(func: types.FunctionType):
        if hname is None:
            name = func.__name__
        else:
            name = hname
        nick_ping_registry[hname] = func
        return func
    return real_dec


import types


post_created_registry = {}
topic_created_registry = {}
nick_ping_registry = {}


def post_handler(name):
    """
    Decorator for adding a new post handler.
    """

    def real_dec(func: types.FunctionType):
        if name is None:
            name = func.__name__
        post_created_registry[name] = name
        return func
    return real_dec

def topic_handler(name):
    """
    Decorator for adding a new topic handler.

    You probably won't need this.
    """

    def real_dec(func: types.FunctionType):
        if name is None:
            name = func.__name__
        topic_created_registry[name] = name
        return func
    return real_dec


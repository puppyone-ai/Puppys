from functools import wraps


def custom_partial(func, *args, **kwargs):
    @wraps(func)
    def wrapped(*args2, **kwargs2):
        return func(*args, *args2, **kwargs, **kwargs2)
    return wrapped

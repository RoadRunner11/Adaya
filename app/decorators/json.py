from functools import wraps

def as_json(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        print(*args)
        print(**kwargs)
        return function(*args, **kwargs)
    return wrapper
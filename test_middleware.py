from functools import wraps

def middlware(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        print("XDXDDXXD")
        return f(":)", *args, **kwargs)
    return decorated
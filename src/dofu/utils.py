import contextlib


def deprecated(func=None, *, reason: str = ""):
    """
    Decorator to mark a function as deprecated.
    """

    def decorator(fn):
        def wrapper(*args, **kwargs):
            if reason:
                print(f"WARNING: {fn.__name__} is deprecated: {reason}")
            else:
                print(f"WARNING: {fn.__name__} is deprecated.")
            return fn(*args, **kwargs)

        return wrapper

    if func is not None:
        return decorator(func)

    return decorator


@contextlib.contextmanager
def supress(*exceptions):
    """
    Suppress exceptions.

    :param exceptions: The exceptions to suppress.
    """
    try:
        yield

    except Exception as e:
        if not isinstance(e, exceptions):
            raise

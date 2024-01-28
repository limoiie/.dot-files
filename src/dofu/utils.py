import contextlib
import logging

import typing as t

_logger = logging.getLogger(__name__)


def deprecated(func=None, *, reason: str = ""):
    """
    Decorator to mark a function as deprecated.
    """

    def decorator(fn):
        def wrapper(*args, **kwargs):
            if reason:
                _logger.warning(f"{fn.__name__} is deprecated: {reason}")
            else:
                _logger.warning(f"{fn.__name__} is deprecated.")
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


def find(iterable: t.Iterable, value=None, *, key=None, pred=None, default=None):
    """
    Fetch an element from an iterable.

    There are two ways to fetch an element:
    - If `value` is specified,
      the element that equals to the value will be returned.
      If `key` is provided, the comparison will be performed on the key .
    - If `pred` is specified, any element that satisfies the predicate will be returned.

    :param iterable: An iterable for searching from
    :param value: If specified, the element with the value will be returned.
    :param key: If specified, the comparison will be done with the key of the element.
    :param pred: If specified, the comparison will be done with the predicate.
    :param default: The default value to return if no element is found.
    :return: The element that matches the condition. None if no element is found.
    """
    if pred is not None:
        for element in iterable:
            if pred(element):
                return element
    else:
        key = key or (lambda x: x)
        value = key(value)
        for element in iterable:
            if key(element) == value:
                return element
    return default

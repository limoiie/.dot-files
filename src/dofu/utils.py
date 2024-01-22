import contextlib
import os
import shutil
import subprocess


@contextlib.contextmanager
def file_update_guarder(path: os.PathLike):
    """
    Backup a file and restore it if an exception is raised.
    Otherwise, delete it after the context exited successfully.
    """

    backup_path = str(path) + ".lock"
    while os.path.exists(backup_path):
        backup_path += ".lock"

    if os.path.exists(path):
        shutil.move(path, backup_path)

    try:
        yield backup_path

    except Exception:
        if os.path.exists(path):
            os.remove(path)
        if os.path.exists(backup_path):
            shutil.move(backup_path, path)

        raise

    else:
        os.remove(backup_path)


def do_commands_exist(*commands: str):
    """
    Check if the given commands exist.

    :param commands: The commands to check.
    :return: True if all the commands exist, False otherwise.
    """
    for command in commands:
        if subprocess.call(f"command -v {command}") != 0:
            return False
    return True


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

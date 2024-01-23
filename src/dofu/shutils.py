import contextlib
import os
import shutil
import subprocess

from .options import Options

CompletedProcess = subprocess.CompletedProcess


def mkdirs(path, mode=0o777, exist_ok=False):
    if Options.instance().dry_run:
        print(f"mkdirs {path}")
        return

    return os.makedirs(path, mode=mode, exist_ok=exist_ok)


def link(src, dst, *, follow_symlinks=True):
    if Options.instance().dry_run:
        print(f"link {src} to {dst}")
        return

    return os.link(src, dst, follow_symlinks=follow_symlinks)


def unlink(path, *, dir_fd=None):
    if Options.instance().dry_run:
        print(f"unlink {path}")
        return

    return os.unlink(path, dir_fd=dir_fd)


def remove(path, *, dir_fd=None):
    if Options.instance().dry_run:
        print(f"remove {path}")
        return

    return os.remove(path, dir_fd=dir_fd)


def rmdir(path, *, dir_fd=None):
    if Options.instance().dry_run:
        print(f"rmdir {path}")
        return

    return os.rmdir(path, dir_fd=dir_fd)


def move(src, dst):
    if Options.instance().dry_run:
        print(f"move {src} to {dst}")
        return

    return shutil.move(src, dst)


def rmtree(path, ignore_errors=False, onerror=None):
    if Options.instance().dry_run:
        print(f"remove {path}")
        return

    return shutil.rmtree(path, ignore_errors=ignore_errors, onerror=onerror)


def call(sh: str, *args, **kwargs):
    if Options.instance().dry_run:
        print(f"{sh} {args}")
        return 0

    return subprocess.call(sh, *args, **kwargs)


def run(sh: str, *args, **kwargs):
    if Options.instance().dry_run:
        print(f"{sh} {args}")
        return CompletedProcess([sh, *args] if args else sh, 0, None, None)

    return subprocess.run(sh, *args, **kwargs)


def check_output(sh: str, *args, **kwargs):
    if Options.instance().dry_run:
        print(f"{sh} {args}")
        if kwargs.get("encoding", None):
            return ""
        return b""

    return subprocess.check_output(sh, *args, **kwargs)


def check_call(sh: str, *args, **kwargs):
    if Options.instance().dry_run:
        print(f"{sh} {args}")
        return 0

    return subprocess.check_call(sh, *args, **kwargs)


@contextlib.contextmanager
def file_update_guarder(path: os.PathLike):
    """
    A context manager that guards a file from being updated.

    This context manager will dispatch a temporary path for updating with.
    After the context manager exits,
    the temporary file will be moved to the given path.
    If any exception occurs, the temporary file will be removed.

    :param path: The path to the file.
    """

    temp_path = str(path) + ".dofu.tmp"
    while os.path.exists(temp_path):
        temp_path += ".tmp"

    try:
        yield temp_path

    except Exception:
        if os.path.exists(temp_path):
            remove(temp_path)

        raise

    finally:
        if Options.instance().dry_run:
            os.remove(temp_path)

    if os.path.exists(path):
        remove(path)
    move(temp_path, path)


def do_commands_exist(*commands: str):
    """
    Check if the given commands exist.

    :param commands: The commands to check.
    :return: True if all the commands exist, False otherwise.
    """
    for command in commands:
        if subprocess.call(f"command -v {command}", shell=True) != 0:
            return False
    return True

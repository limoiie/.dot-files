import contextlib
import fileinput
import os
import shutil
import subprocess

from .options import Options

CompletedProcess = subprocess.CompletedProcess


def mkdirs(path, mode=0o777, exist_ok=False):
    if Options.instance().dry_run:
        print(f"mkdir -p {path}")
        return

    return os.makedirs(path, mode=mode, exist_ok=exist_ok)


def link(src, dst, *, follow_symlinks=True):
    if Options.instance().dry_run:
        print(f"ln {src} to {dst}")
        return

    return os.link(src, dst, follow_symlinks=follow_symlinks)


def symlink(src, dst, target_is_directory=False, *, dir_fd=None):
    if Options.instance().dry_run:
        print(f"ln -s {src} to {dst}")
        return

    return os.symlink(src, dst, target_is_directory=target_is_directory, dir_fd=dir_fd)


def unlink(path, *, dir_fd=None):
    if Options.instance().dry_run:
        print(f"unlink {path}")
        return

    return os.unlink(path, dir_fd=dir_fd)


def remove(path, *, dir_fd=None):
    if Options.instance().dry_run:
        print(f"rm {path}")
        return

    return os.remove(path, dir_fd=dir_fd)


def rmdir(path, *, dir_fd=None):
    if Options.instance().dry_run:
        print(f"rm -r {path}")
        return

    return os.rmdir(path, dir_fd=dir_fd)


def move(src, dst):
    if Options.instance().dry_run:
        print(f"mv {src} {dst}")
        return

    return shutil.move(src, dst)


def rmtree(path, ignore_errors=False, onerror=None):
    if Options.instance().dry_run:
        print(f"rm -rf {path}")
        return

    return shutil.rmtree(path, ignore_errors=ignore_errors, onerror=onerror)


def call(sh: str, *args, **kwargs):
    if Options.instance().dry_run:
        print(f"{sh} {args}")
        return 0

    return subprocess.call(sh, *args, shell=True, **kwargs)


def run(sh: str, *args, **kwargs):
    if Options.instance().dry_run:
        print(f"{sh} {args}")
        return CompletedProcess([sh, *args] if args else sh, 0, None, None)

    return subprocess.run(sh, *args, shell=True, **kwargs)


def check_output(sh: str, *args, **kwargs):
    if Options.instance().dry_run:
        print(f"{sh} {args}")
        if kwargs.get("encoding", None):
            return ""
        return b""

    return subprocess.check_output(sh, *args, shell=True, **kwargs)


def check_call(sh: str, *args, **kwargs):
    if Options.instance().dry_run:
        print(f"{sh} {args}")
        return 0

    return subprocess.check_call(sh, *args, shell=True, **kwargs)


def input_file(
    files,
    inplace=False,
    backup=".dofu.bak",
    *,
    mode="r",
    openhook=None,
    encoding=None,
    errors=None,
):
    if Options.instance().dry_run:
        if inplace:
            print(f"The file {files} will be updated inplace as:")
        inplace = False

    return fileinput.input(
        files,
        inplace=inplace,
        backup=backup,
        mode=mode,
        openhook=openhook,
        encoding=encoding,
        errors=errors,
    )


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
            os.remove(temp_path)

        raise

    if Options.instance().dry_run:
        if os.path.exists(temp_path):
            os.remove(temp_path)

        print(f'move {temp_path} to {path}')
        return

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

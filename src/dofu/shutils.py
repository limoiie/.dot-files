import abc
import contextlib
import dataclasses
import difflib
import fileinput
import io
import logging
import os
import shutil
import subprocess
import typing as t

from dofu import gum
from dofu.options import Options, Strategy

_logger = logging.getLogger(__name__ + "[/] [green]RUN")
_dryrun_logger = logging.getLogger(__name__ + "[/] [blue]DRYRUN")

CompletedProcess = subprocess.CompletedProcess


def copy(src, dst, *, follow_symlinks=True):
    EnsurePathExists(action=f"cp", path=src, is_dir=False)()
    EnsurePathNotExists(action=f"cp", path=dst)()

    if Options.instance().dry_run:
        _dryrun_logger.info(f"cp {src} {dst}")
        return None

    _logger.info(f"cp {src} {dst}")
    return shutil.copy(src, dst, follow_symlinks=follow_symlinks)


def link(src, dst, *, follow_symlinks=True):
    EnsurePathExists(action=f"ln", path=src, is_dir=False)()
    EnsurePathNotExists(action=f"ln", path=dst)()

    if Options.instance().dry_run:
        _dryrun_logger.info(f"ln {src} {dst}")
        return None

    _logger.info(f"ln {src} {dst}")
    return os.link(src, dst, follow_symlinks=follow_symlinks)


def symlink(src, dst, target_is_directory=False, *, dir_fd=None):
    EnsurePathExists(action=f"ln -s", path=src, is_dir=target_is_directory)()
    EnsurePathNotExists(action=f"ln -s", path=dst)()

    if Options.instance().dry_run:
        _dryrun_logger.info(f"ln -s {src} {dst}")
        return None

    _logger.info(f"ln -s {src} {dst}")
    return os.symlink(src, dst, target_is_directory=target_is_directory, dir_fd=dir_fd)


def unlink(path, *, dir_fd=None):
    EnsurePathExists(action=f"unlink", path=path, is_dir=False, to_del=True)()

    if Options.instance().dry_run:
        _dryrun_logger.info(f"unlink {path}")
        return None

    _logger.info(f"unlink {path}")
    return os.unlink(path, dir_fd=dir_fd)


def mkdirs(path, mode=0o777, exist_ok=False):
    if not exist_ok:
        EnsurePathNotExists(action=f"mkdir -p", path=path)()

    if Options.instance().dry_run:
        _dryrun_logger.info(f"mkdir -p {path}")
        return None

    _logger.info(f"mkdir -p {path}")
    return os.makedirs(path, mode=mode, exist_ok=exist_ok)


def move(src, dst):
    EnsurePathExists(action=f"mv", path=src)()
    EnsurePathNotExists(action=f"mv", path=dst)()

    if Options.instance().dry_run:
        _dryrun_logger.info(f"mv {src} {dst}")
        return None

    _logger.info(f"mv {src} {dst}")
    return shutil.move(src, dst)


def remove(path, *, dir_fd=None):
    EnsurePathExists(action=f"rm", path=path, is_dir=False, to_del=True)()

    if Options.instance().dry_run:
        _dryrun_logger.info(f"rm {path}")
        return None

    _logger.info(f"rm {path}")
    return os.remove(path, dir_fd=dir_fd)


def rmdir(path, *, dir_fd=None):
    EnsurePathExists(action=f"rmdir", path=path, is_dir=True, to_del=True)()

    if Options.instance().dry_run:
        _dryrun_logger.info(f"rm -r {path}")
        return None

    _logger.info(f"rm -r {path}")
    return os.rmdir(path, dir_fd=dir_fd)


def rmtree(path, ignore_errors=False, onerror=None):
    EnsurePathExists(action=f"mv", path=path, to_del=True)()

    if Options.instance().dry_run:
        _dryrun_logger.info(f"rm -rf {path}")
        return None

    _logger.info(f"rm -rf {path}")
    return shutil.rmtree(path, ignore_errors=ignore_errors, onerror=onerror)


def call(sh: str, *args, **kwargs):
    if Options.instance().dry_run:
        _dryrun_logger.info(f"{sh} {args}")
        return 0

    _logger.info(f"{sh} {args}")
    return subprocess.call(sh, *args, shell=True, **kwargs)


def call_no_side_effect(sh: str, *args, **kwargs):
    if Options.instance().dry_run:
        _dryrun_logger.info(f"{sh} {args}")
        return 0

    _logger.info(f"{sh} {args}")
    return subprocess.call(sh, *args, shell=True, **kwargs)


def run(sh: str, *args, **kwargs):
    if Options.instance().dry_run:
        _dryrun_logger.info(f"{sh} {args}")
        return CompletedProcess([sh, *args] if args else sh, 0, None, None)

    _logger.info(f"{sh} {args}")
    return subprocess.run(sh, *args, shell=True, **kwargs)


def run_no_side_effect(sh: str, *args, **kwargs):
    return subprocess.run(sh, *args, shell=True, **kwargs)


def check_output(sh: str, *args, **kwargs):
    if Options.instance().dry_run:
        _dryrun_logger.info(f"{sh} {args}")
        if kwargs.get("encoding", None):
            return ""
        return b""

    _logger.info(f"{sh} {args}")
    return subprocess.check_output(sh, *args, shell=True, **kwargs)


def check_output_no_side_effect(sh: str, *args, **kwargs):
    return subprocess.check_output(sh, *args, shell=True, **kwargs)


def check_call(sh: str, *args, **kwargs):
    if Options.instance().dry_run:
        _dryrun_logger.info(f"{sh} {args}")
        return 0

    _logger.info(f"{sh} {args}")
    return subprocess.check_call(sh, *args, shell=True, **kwargs)


def check_call_no_side_effect(sh: str, *args, **kwargs):
    return subprocess.check_call(sh, *args, shell=True, **kwargs)


@contextlib.contextmanager
def input_file(
    filepath,
    inplace=False,
    backup=".dofu.bak",
    *,
    mode="r",
    openhook=None,
    encoding=None,
    errors=None,
):
    ensure_path_exists(action=f"input_file", path=filepath, is_dir=False)

    updated_lines = []
    dry_run = Options.instance().dry_run
    with fileinput.input(
        filepath,
        inplace=not dry_run and inplace,
        backup=backup,
        mode=mode,
        openhook=openhook,
        encoding=encoding,
        errors=errors,
    ) as file:
        if dry_run and inplace:
            with io.StringIO() as tmp:
                with contextlib.redirect_stdout(tmp):
                    yield file
                tmp.seek(0)
                updated_lines = tmp.readlines()

        else:
            yield file

    if dry_run and inplace:
        with open(filepath, "r") as origin:
            diff_lines = difflib.unified_diff(
                origin.readlines(),
                updated_lines,
                fromfile=str(filepath),
                tofile=str(filepath) + "<inplace>",
            )

        diff_text = "".join(diff_lines).rstrip() or "No change!"
        _dryrun_logger.info(f"update {str(filepath)} as:\n{diff_text}")


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

    temp_path = backup_path(str(path), suffix=".dofu.tmp")

    try:
        yield temp_path

    except Exception:
        if os.path.exists(temp_path):
            os.remove(temp_path)

        raise

    if Options.instance().dry_run:
        # dry run, remove the changes
        if os.path.exists(temp_path):
            os.remove(temp_path)
    else:
        # replace the original file with the temporary file
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
        if (
            subprocess.call(
                f"command -v {command}",
                shell=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            != 0
        ):
            return False
    return True


def command_path(command: str) -> str:
    return subprocess.check_output(
        f"command -v {command}", shell=True, encoding="utf-8"
    ).strip()


@dataclasses.dataclass
class Ensure(abc.ABC):
    action: str

    def __call__(self, *args, **kwargs):
        return self.ensure()

    def ensure(self):
        strategy = Options.instance().strategy
        while strategy is not None and not self.condition():
            if Options.instance().dry_run:
                return
            strategy = self.strategy_execs[strategy.value]()

    @abc.abstractmethod
    def condition(self) -> bool:
        pass

    def interactive(self) -> t.Optional[Strategy]:
        strategy = gum.choose(
            "TRY-AGAIN",
            *Strategy.all_decidable_names(),
            header=f"{self.failure_message()}, what to do?",
            selected=[Strategy.AUTO.name],
        ).strip()

        # try again
        if strategy == "TRY-AGAIN":
            return Strategy.ASK

        # apply chosen strategy
        strategy = Strategy[strategy]
        return self.strategy_execs[strategy.value]()

    @abc.abstractmethod
    def overwrite(self) -> t.Optional[Strategy]:
        pass

    @abc.abstractmethod
    def non_intrusive(self) -> t.Optional[Strategy]:
        pass

    def cancel(self) -> None:
        raise RuntimeError(self.failure_message())

    @property
    def strategy_execs(self):
        return [
            self.interactive,
            self.overwrite,
            self.non_intrusive,
            self.cancel,
        ]

    def failure_message(self) -> str:
        return f"Failed to {self.action}: {self.failure_reason()}"

    @abc.abstractmethod
    def failure_reason(self):
        pass


@dataclasses.dataclass
class EnsurePathExists(Ensure):
    path: str
    """
    The path to be checked.
    """

    is_dir: bool = None
    """
    Whether the path is a directory.
    """

    to_del: bool = False
    """
    Whether the path is to be deleted.
    """

    def condition(self) -> bool:
        return os.path.exists(self.path)

    def overwrite(self):
        return self.non_intrusive()

    def non_intrusive(self):
        if self.to_del:
            return
        # create a new file
        open(self.path, "w+").close()

    def failure_reason(self):
        return f"{self.path} not exists"


@dataclasses.dataclass
class EnsurePathNotExists(Ensure):
    path: str
    """
    The path to be checked.
    """

    def condition(self) -> bool:
        return not os.path.exists(self.path)

    def overwrite(self):
        if os.path.islink(self.path) or os.path.isfile(self.path):
            os.remove(self.path)
        elif os.path.isdir(self.path):
            shutil.rmtree(self.path)

    def non_intrusive(self):
        shutil.move(self.path, backup_path(self.path))

    def failure_reason(self):
        return f"{self.path} already exists"


def ensure_path_exists(
    action: str, path: str, is_dir: bool = None, to_del: bool = False
):
    return EnsurePathExists(
        action=action,
        path=path,
        is_dir=is_dir,
        to_del=to_del,
    )()


def ensure_path_not_exists(action: str, path: str):
    return EnsurePathNotExists(
        action=action,
        path=path,
    )()


def backup_path(path, *, suffix=".dofu.bak"):
    part_suffix = suffix[suffix.rfind(".") :]
    unoccupied_path = f"{path}{suffix}"
    while os.path.exists(unoccupied_path):
        unoccupied_path += part_suffix
    return unoccupied_path

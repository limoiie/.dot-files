import abc
import dataclasses
import os
import pathlib
import re
import sys
import typing as t

from dofu import shutils
from dofu.options import Options
from .utils import deprecated


@dataclasses.dataclass
class ExecutionResult:
    cmdline: str
    retcode: int
    stdout: t.Optional[bytes] = None
    stderr: t.Optional[bytes] = None

    def __bool__(self):
        return self.retcode == 0

    @staticmethod
    def of_result(result: shutils.CompletedProcess):
        cmdline = result.args
        if not isinstance(result.args, str):
            cmdline = " ".join(result.args)

        return ExecutionResult(
            cmdline=cmdline,
            retcode=result.returncode,
            stdout=result.stdout,
            stderr=result.stderr,
        )


@dataclasses.dataclass
class UndoableCommand:
    # ret: t.Optional[ExecutionResult]

    def exec(self) -> ExecutionResult:
        try:
            return self._exec()

        except Exception as e:
            return self._failure_result(e)

    def undo(self) -> t.Optional[ExecutionResult]:
        try:
            return self._undo()

        except Exception as e:
            return self._failure_result(e)

    @abc.abstractmethod
    def cmdline(self) -> str:
        pass

    @abc.abstractmethod
    def _exec(self) -> ExecutionResult:
        pass

    @abc.abstractmethod
    def _undo(self) -> None:
        pass

    @abc.abstractmethod
    def spec_tuple(self):
        pass

    def _failure_result(self, exc):
        return ExecutionResult(
            cmdline=self.cmdline(), retcode=1, stderr=str(exc).encode("utf-8")
        )

    def _success_result(self, stdout=None, stderr=None):
        return ExecutionResult(
            cmdline=self.cmdline(), retcode=0, stdout=stdout, stderr=stderr
        )


@dataclasses.dataclass
class UCSymlink(UndoableCommand):
    src: str
    dst: str
    real_dst: str = None
    ret: t.Optional[ExecutionResult] = None

    def cmdline(self) -> str:
        return f"ln -s {self.src} {self.dst}"

    def _exec(self):
        _assert_exists(self.src, "Failed to ln -s", "src")
        _assert_not_exists(self.dst, "Failed to ln -s", "dst")

        shutils.symlink(self.src, self.dst)
        self.ret = self._success_result()
        self.real_dst = self.dst
        return self.ret

    def _undo(self):
        _assert_exists(self.real_dst, "Failed to unlink", "dst")
        _assert_exists(self.src, "Failed to unlink", "src")

        shutils.unlink(self.real_dst)
        self.real_dst = None
        self.ret = None

    def spec_tuple(self):
        return self.src, self.dst


@dataclasses.dataclass
class UCLink(UndoableCommand):
    src: str
    dst: str
    real_dst: str = None
    ret: t.Optional[ExecutionResult] = None

    def cmdline(self) -> str:
        return f"ln {self.src} {self.dst}"

    def _exec(self):
        _assert_exists(self.src, "Failed to ln", "src")
        _assert_not_exists(self.dst, "Failed to ln", "dst")

        shutils.link(self.src, self.dst)
        self.ret = self._success_result()
        self.real_dst = self.dst
        return self.ret

    def _undo(self):
        _assert_exists(self.real_dst, "Failed to unlink", "dst")
        _assert_exists(self.src, "Failed to unlink", "src")

        shutils.unlink(self.real_dst)
        self.real_dst = None
        self.ret = None

    def spec_tuple(self):
        return self.src, self.dst


@dataclasses.dataclass
class UCBackupMv(UndoableCommand):
    path: str
    backup_path: str = None
    ret: t.Optional[ExecutionResult] = None

    def cmdline(self) -> str:
        return f"backup-mv {self.path} {self.backup_path}"

    def _exec(self):
        _assert_exists(self.path, "Failed to backup mv", "path")

        backup_path = f"{self.path}.dofu.bak"
        while os.path.exists(backup_path):
            backup_path += ".bak"

        shutils.move(self.path, backup_path)
        self.ret = self._success_result()
        self.backup_path = backup_path
        return self.ret

    def _undo(self):
        _assert_exists(self.backup_path, "Failed to undo backup mv", "dst")
        _assert_not_exists(self.path, "Failed to undo backup mv", "src")

        shutils.move(self.backup_path, self.path)
        self.backup_path = None
        self.ret = None

    def spec_tuple(self):
        return (self.path,)


@dataclasses.dataclass
class UCMkdir(UndoableCommand):
    path: str
    last_exist_path: t.Optional[str] = None
    ret: t.Optional[ExecutionResult] = None

    def cmdline(self) -> str:
        return f"mkdir -p {self.path}"

    def _exec(self):
        path = pathlib.Path(self.path)
        if path.exists():
            self.last_exist_path = None
        else:
            last_exist_path = path
            while not last_exist_path.exists():
                last_exist_path = last_exist_path.parent

            shutils.mkdirs(path)
            self.last_exist_path = last_exist_path

        self.ret = self._success_result()
        return self.ret

    def _undo(self):
        if self.last_exist_path and os.path.exists(self.last_exist_path):
            path = pathlib.Path(self.path)
            while not path.samefile(self.last_exist_path):
                if path.exists():
                    shutils.rmdir(path)
                path = path.parent

        self.last_exist_path = None
        self.ret = None

    def spec_tuple(self):
        return (self.path,)


@dataclasses.dataclass
class UCMove(UndoableCommand):
    src: str
    dst: str
    real_dst: str = None
    ret: t.Optional[ExecutionResult] = None

    def cmdline(self) -> str:
        return f"mv {self.src} {self.dst}"

    def _exec(self):
        _assert_exists(self.src, "Failed to mv", "src")
        _assert_not_exists(self.dst, "Failed to mv", "dst")

        shutils.move(self.src, self.dst)
        self.ret = self._success_result()
        self.real_dst = self.dst
        return self.ret

    def _undo(self):
        _assert_exists(self.real_dst, "Failed to undo mv", "dst")
        _assert_not_exists(self.src, "Failed to undo mv", "src")

        shutils.move(self.real_dst, self.src)
        self.real_dst = None
        self.ret = None

    def spec_tuple(self):
        return self.src, self.dst


@deprecated(reason="Use dofu.requirement.GitRepoRequirement instead.")
@dataclasses.dataclass
class UCGitClone(UndoableCommand):
    url: str
    path: t.Optional[str] = None
    depth: t.Optional[int] = None
    ret: t.Optional[ExecutionResult] = None

    def cmdline(self) -> str:
        cmd = "git clone"
        cmd = cmd + f" --depth={self.depth}" if self.depth else cmd
        return f"{cmd} {self.url} {self.path}"

    def _exec(self):
        _assert_not_exists(self.path, "Failed to git clone", "path")

        res = shutils.run(self.cmdline(), shell=True)
        self.ret = ExecutionResult.of_result(res)
        return self.ret

    def _undo(self):
        _assert_exists(self.path, "Failed to undo git clone", "path")

        shutils.rmtree(self.path)
        self.ret = None

    def spec_tuple(self):
        return self.url, self.path


@deprecated(reason="Use dofu.requirement.GitRepoRequirement instead.")
@dataclasses.dataclass
class UCGitPull(UndoableCommand):
    path: str
    ret: t.Optional[ExecutionResult] = None

    def cmdline(self) -> str:
        return f"git pull"

    def _exec(self):
        _assert_not_exists(self.path, "Failed to git pull", "repo")

        res = shutils.run(self.cmdline(), shell=True, cwd=self.path)
        self.ret = ExecutionResult.of_result(res)
        return self.ret

    def _undo(self):
        self.ret = None

    def spec_tuple(self):
        return (self.path,)


@dataclasses.dataclass
class UCReplaceLine(UndoableCommand):
    path: str
    pattern: str
    new_line: str
    replaced_line: t.Optional[str] = None
    ret: t.Optional[ExecutionResult] = None

    def cmdline(self) -> str:
        return f"replace-line {self.pattern} in {self.path} with {self.new_line}"

    def _exec(self):
        _assert_exists(self.path, "Failed to replace line", "path")

        replaced_line = None
        pattern = re.compile(self.pattern)
        for line in shutils.input_file(self.path, inplace=True):
            if replaced_line is None and re.search(pattern, line):
                replaced_line = line
                new_line = self.new_line.rstrip("\n")
                line = (new_line + "\n") if line.endswith("\n") else new_line
            sys.stdout.write(line)

        self.replaced_line = replaced_line
        self.ret = self._success_result()
        return self.ret

    def _undo(self):
        _assert_exists(self.path, "Failed to replace line", "path")

        for line in shutils.input_file(self.path, inplace=True):
            if line.startswith(self.new_line):
                line = self.replaced_line
            sys.stdout.write(line)

    def spec_tuple(self):
        return self.path, self.pattern, self.new_line


def _assert_exists(path, msg, name="path"):
    if Options.instance().dry_run:
        return

    if not os.path.exists(path):
        raise RuntimeError(f"{msg}: {name} {path} not exists")


def _assert_not_exists(path, msg, name="path"):
    if Options.instance().dry_run:
        return

    if os.path.exists(path):
        raise RuntimeError(f"{msg}: {name} {path} already exists")

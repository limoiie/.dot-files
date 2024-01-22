import abc
import dataclasses
import fileinput
import os
import pathlib
import re
import shutil
import subprocess
import sys
import typing as t

from .utils import deprecated, supress


@dataclasses.dataclass
class ExecutionResult:
    cmdline: str
    retcode: int
    stdout: t.Optional[bytes] = None
    stderr: t.Optional[bytes] = None

    def __bool__(self):
        return self.retcode == 0

    @staticmethod
    def of_result(result: subprocess.CompletedProcess):
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
    ret: t.Optional[ExecutionResult]

    @abc.abstractmethod
    def exec(self) -> ExecutionResult:
        pass

    @abc.abstractmethod
    def undo(self):
        pass

    @abc.abstractmethod
    def spec_tuple(self):
        pass


@dataclasses.dataclass
class UCLink(UndoableCommand):
    src: str
    dst: str
    real_dst: str = None
    ret: t.Optional[ExecutionResult] = None

    def exec(self):
        _assert_exists(self.src, "Failed to ln", "src")
        _assert_not_exists(self.dst, "Failed to ln", "dst")

        os.link(self.src, self.dst)
        self.ret = ExecutionResult(
            cmdline=f"ln -s {self.src} {self.dst}",
            retcode=0,
            stdout=None,
            stderr=None,
        )
        self.real_dst = self.dst
        return self.ret

    def undo(self):
        _assert_exists(self.real_dst, "Failed to unlink", "dst")
        _assert_not_exists(self.src, "Failed to unlink", "src")

        os.unlink(self.real_dst)
        self.real_dst = None
        self.ret = None

    def spec_tuple(self):
        return self.src, self.dst


@dataclasses.dataclass
class UCBackupMv(UndoableCommand):
    path: str
    backup_path: str = None
    ret: t.Optional[ExecutionResult] = None

    def exec(self):
        _assert_exists(self.path, "Failed to backup mv", "path")

        backup_path = f"{self.path}.dofu.bak"
        while os.path.exists(backup_path):
            backup_path += ".bak"

        shutil.move(self.path, backup_path)
        self.ret = ExecutionResult(
            cmdline=f"mv {self.path} {self.backup_path}",
            retcode=0,
            stdout=None,
            stderr=None,
        )
        self.backup_path = backup_path
        return self.ret

    def undo(self):
        _assert_exists(self.backup_path, "Failed to undo backup mv", "dst")
        _assert_not_exists(self.path, "Failed to undo backup mv", "src")

        shutil.move(self.backup_path, self.path)
        self.backup_path = None
        self.ret = None

    def spec_tuple(self):
        return (self.path,)


@dataclasses.dataclass
class UCMkdir(UndoableCommand):
    path: str
    created_path: t.Optional[str] = None
    ret: t.Optional[ExecutionResult] = None

    def exec(self):
        path = pathlib.Path(self.path)
        if path.exists():
            self.created_path = None
        else:
            while not path.exists():
                path = path.parent

            os.makedirs(path)
            self.created_path = path

        self.ret = ExecutionResult(
            cmdline=f"mkdir -p {self.path}",
            retcode=0,
            stdout=None,
            stderr=None,
        )
        return self.ret

    def undo(self):
        if os.path.exists(self.created_path):
            with supress(FileNotFoundError, OSError):
                os.rmdir(self.created_path)
        self.created_path = None
        self.ret = None

    def spec_tuple(self):
        return (self.path,)


@dataclasses.dataclass
class UCMove(UndoableCommand):
    src: str
    dst: str
    real_dst: str = None
    ret: t.Optional[ExecutionResult] = None

    def exec(self):
        _assert_exists(self.src, "Failed to mv", "src")
        _assert_not_exists(self.dst, "Failed to mv", "dst")

        shutil.move(self.src, self.dst)
        self.ret = ExecutionResult(
            cmdline=f"mv {self.src} {self.dst}",
            retcode=0,
            stdout=None,
            stderr=None,
        )
        self.real_dst = self.dst
        return self.ret

    def undo(self):
        _assert_exists(self.real_dst, "Failed to undo mv", "dst")
        _assert_not_exists(self.src, "Failed to undo mv", "src")

        shutil.move(self.real_dst, self.src)
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

    def exec(self):
        _assert_not_exists(self.path, "Failed to git clone", "path")

        cmd = "git clone"
        cmd = cmd + f" --depth={self.depth}" if self.depth else cmd
        res = subprocess.run(f"{cmd} {self.url} {self.path}", shell=True)
        self.ret = ExecutionResult.of_result(res)
        return self.ret

    def undo(self):
        _assert_exists(self.path, "Failed to undo git clone", "path")

        shutil.rmtree(self.path)
        self.ret = None

    def spec_tuple(self):
        return self.url, self.path


@deprecated(reason="Use dofu.requirement.GitRepoRequirement instead.")
@dataclasses.dataclass
class UCGitPull(UndoableCommand):
    path: str
    ret: t.Optional[ExecutionResult] = None

    def exec(self):
        _assert_not_exists(self.path, "Failed to git pull", "repo")

        cmd = "git pull"
        res = subprocess.run(f"{cmd}", shell=True, cwd=self.path)
        self.ret = ExecutionResult.of_result(res)
        return self.ret

    def undo(self):
        self.ret = None

    def spec_tuple(self):
        return (self.path,)


@dataclasses.dataclass
class UCReplaceLine(UndoableCommand):
    path: str
    line_pat: str
    new_line: str
    replaced_line: t.Optional[str] = None
    ret: t.Optional[ExecutionResult] = None

    def exec(self):
        _assert_exists(self.path, "Failed to replace line", "path")

        replaced_line = None
        pat = re.compile(self.line_pat)
        for line in fileinput.input(self.path, inplace=True):
            if replaced_line is None and re.search(pat, line):
                replaced_line = line
                line = self.new_line.rsplit("\n") + "\n"
            sys.stdout.write(line)

        self.replaced_line = replaced_line
        self.ret = ExecutionResult(
            cmdline=f"replace line {self.line_pat} in {self.path} with {self.new_line}",
            retcode=0,
            stdout=None,
            stderr=None,
        )

    def undo(self):
        _assert_exists(self.path, "Failed to replace line", "path")

        for line in fileinput.input(self.path, inplace=True):
            if line.startswith(self.new_line):
                line = self.replaced_line
            sys.stdout.write(line)

    def spec_tuple(self):
        return self.path, self.line_pat, self.new_line


def _assert_exists(path, msg, name="path"):
    if not os.path.exists(path):
        raise RuntimeError(f"{msg}: {name} {path} not exists")


def _assert_not_exists(path, msg, name="path"):
    if os.path.exists(path):
        raise RuntimeError(f"{msg}: {name} {path} already exists")

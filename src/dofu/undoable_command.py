import abc
import dataclasses
import subprocess
import typing as t

import autoserde

from dofu import shutils


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

    def to_error(self):
        return subprocess.CalledProcessError(
            returncode=self.retcode,
            cmd=self.cmdline,
            output=self.stdout,
            stderr=self.stderr,
        )


@dataclasses.dataclass
class UndoableCommand(autoserde.Serdeable, abc.ABC):
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

import dataclasses
import typing as t
import os

from dofu import shutils
from dofu.undoable_command import ExecutionResult, UndoableCommand


@dataclasses.dataclass
class UCChSh(UndoableCommand):
    shell: str
    real_shell: str = None
    origin_shell: str = None
    ret: t.Optional[ExecutionResult] = None

    def cmdline(self) -> str:
        return f"chsh -s {self.shell}"

    def _exec(self):
        self.origin_shell = os.environ.get("SHELL")
        shell = shutils.command_path(self.shell)
        shutils.check_call(f"chsh -s ${shell}")
        self.real_shell = shell
        return self.ret

    def _undo(self):
        if self.origin_shell:
            shutils.check_call(f"chsh -s ${self.origin_shell}")
        self.origin_shell = None
        self.ret = None

    def spec_tuple(self):
        return (self.shell,)

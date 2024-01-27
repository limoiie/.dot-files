import dataclasses
import typing as t

from dofu import shutils
from dofu.undoable_command import ExecutionResult, UndoableCommand


@dataclasses.dataclass
class UCSymlink(UndoableCommand):
    src: str
    dst: str
    real_dst: str = None
    ret: t.Optional[ExecutionResult] = None

    def cmdline(self) -> str:
        return f"ln -s {self.src} {self.dst}"

    def _exec(self):
        shutils.symlink(self.src, self.dst)
        self.ret = self._success_result()
        self.real_dst = self.dst
        return self.ret

    def _undo(self):
        shutils.unlink(self.real_dst)
        self.real_dst = None
        self.ret = None

    def spec_tuple(self):
        return self.src, self.dst

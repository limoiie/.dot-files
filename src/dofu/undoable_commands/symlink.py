import dataclasses
import os
import typing as t

from dofu import shutils
from dofu.undoable_command import ExecutionResult, UndoableCommand


@dataclasses.dataclass
class UCSymlink(UndoableCommand):
    src: str
    dst: str
    real_dst: t.Optional[str] = None
    ret: t.Optional[ExecutionResult] = None

    def cmdline(self) -> str:
        return f"ln -s {self.src} {self.dst}"

    def _exec(self):
        if os.path.islink(self.dst) and os.readlink(self.dst) == self.src:
            # already linked, skip
            real_dst = None

        else:
            shutils.symlink(self.src, self.dst)
            real_dst = self.dst

        self.ret = self._success_result()
        self.real_dst = real_dst
        return self.ret

    def _undo(self):
        if self.real_dst:
            shutils.unlink(self.real_dst)
        self.real_dst = None
        self.ret = None

    def spec_tuple(self):
        return self.src, self.dst

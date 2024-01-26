import dataclasses
import typing as t

from dofu import shutils
from dofu.undoable_command import (
    ExecutionResult,
    UndoableCommand,
    assert_exists,
    assert_not_exists,
)


@dataclasses.dataclass
class UCLink(UndoableCommand):
    src: str
    dst: str
    real_dst: str = None
    ret: t.Optional[ExecutionResult] = None

    def cmdline(self) -> str:
        return f"ln {self.src} {self.dst}"

    def _exec(self):
        assert_exists(self.src, "Failed to ln", "src")
        assert_not_exists(self.dst, "Failed to ln", "dst")

        shutils.link(self.src, self.dst)
        self.ret = self._success_result()
        self.real_dst = self.dst
        return self.ret

    def _undo(self):
        assert_exists(self.real_dst, "Failed to unlink", "dst")
        assert_exists(self.src, "Failed to unlink", "src")

        shutils.unlink(self.real_dst)
        self.real_dst = None
        self.ret = None

    def spec_tuple(self):
        return self.src, self.dst

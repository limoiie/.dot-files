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
class UCMove(UndoableCommand):
    src: str
    dst: str
    real_dst: str = None
    ret: t.Optional[ExecutionResult] = None

    def cmdline(self) -> str:
        return f"mv {self.src} {self.dst}"

    def _exec(self):
        assert_exists(self.src, "Failed to mv", "src")
        assert_not_exists(self.dst, "Failed to mv", "dst")

        shutils.move(self.src, self.dst)
        self.ret = self._success_result()
        self.real_dst = self.dst
        return self.ret

    def _undo(self):
        assert_exists(self.real_dst, "Failed to undo mv", "dst")
        assert_not_exists(self.src, "Failed to undo mv", "src")

        shutils.move(self.real_dst, self.src)
        self.real_dst = None
        self.ret = None

    def spec_tuple(self):
        return self.src, self.dst

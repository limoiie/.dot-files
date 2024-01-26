import dataclasses
import os
import typing as t

from dofu import shutils
from dofu.undoable_command import (
    ExecutionResult,
    UndoableCommand,
    assert_exists,
    assert_not_exists,
)


@dataclasses.dataclass
class UCBackupMv(UndoableCommand):
    path: str
    backup_path: str = None
    ret: t.Optional[ExecutionResult] = None

    def cmdline(self) -> str:
        return f"mv {self.path} {self.backup_path}"

    def _exec(self):
        assert_exists(self.path, "Failed to backup mv", "path")

        backup_path = f"{self.path}.dofu.bak"
        while os.path.exists(backup_path):
            backup_path += ".bak"

        shutils.move(self.path, backup_path)
        self.ret = self._success_result()
        self.backup_path = backup_path
        return self.ret

    def _undo(self):
        assert_exists(self.backup_path, "Failed to undo backup mv", "dst")
        assert_not_exists(self.path, "Failed to undo backup mv", "src")

        shutils.move(self.backup_path, self.path)
        self.backup_path = None
        self.ret = None

    def spec_tuple(self):
        return (self.path,)

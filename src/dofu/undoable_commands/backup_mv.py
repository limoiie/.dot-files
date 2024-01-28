import dataclasses
import os
import typing as t

from dofu import shutils
from dofu.undoable_command import ExecutionResult, UndoableCommand


@dataclasses.dataclass
class UCBackupMv(UndoableCommand):
    path: str
    backup_path: t.Optional[str] = None
    ret: t.Optional[ExecutionResult] = None

    def cmdline(self) -> str:
        return f"mv {self.path} {self.backup_path}"

    def _exec(self):
        if os.path.exists(self.path):
            backup_path = shutils.backup_path(self.path)
            shutils.move(self.path, backup_path)
        else:
            backup_path = None

        self.ret = self._success_result()
        self.backup_path = backup_path
        return self.ret

    def _undo(self):
        if self.backup_path is not None:
            shutils.move(self.backup_path, self.path)

        self.backup_path = None
        self.ret = None

    def spec_tuple(self):
        return (self.path,)

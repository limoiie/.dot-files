import dataclasses
import os
import pathlib
import typing as t

from dofu import shutils
from dofu.undoable_command import ExecutionResult, UndoableCommand


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

            shutils.mkdirs(path, exist_ok=True)
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

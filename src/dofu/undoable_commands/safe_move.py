import dataclasses
import os.path
import typing as t

from dofu import env, shutils
from dofu.undoable_command import ExecutionResult, UndoableCommand


@dataclasses.dataclass
class UCSafeMove(UndoableCommand):
    src: str
    dst: str
    real_dst: str = None
    moved: bool = False
    ret: t.Optional[ExecutionResult] = None

    @staticmethod
    def make_home_to_xdg_config(src: str, dst: str):
        return UCSafeMove(
            src=env.user_home_path(src),
            dst=env.xdg_config_path(dst),
        )

    def cmdline(self) -> str:
        return f"[ ! -e {self.src} ] || mv {self.src} {self.dst}"

    def _exec(self):
        if os.path.exists(self.src):
            shutils.move(self.src, self.dst)
            self.moved = True
        else:
            self.moved = False
        self.ret = self._success_result()
        self.real_dst = self.dst
        return self.ret

    def _undo(self):
        if self.moved:
            shutils.move(self.real_dst, self.src)
        self.real_dst = None
        self.ret = None

    def spec_tuple(self):
        return self.src, self.dst

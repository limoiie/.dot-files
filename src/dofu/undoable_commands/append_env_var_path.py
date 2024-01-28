import dataclasses
import re
import sys
import typing as t

from dofu import shutils
from dofu.undoable_command import ExecutionResult, UndoableCommand

_export_path_pattern = re.compile(
    r"export\sPATH=[\'\"]?([^\'\"]*)[\'\"]?:?\$PATH:?[\'\"]?([^\'\"]*)[\'\"]?"
)


@dataclasses.dataclass
class UCAppendEnvVarPath(UndoableCommand):
    path: str
    rc: str
    appended: t.Optional[bool] = None
    ret: t.Optional[ExecutionResult] = None

    def cmdline(self) -> str:
        return f"echo 'export PATH=\"$PATH:{self.path}\" >> {self.rc}'"

    def _exec(self):
        last_export_path_no = -1
        paths_in_path = []
        existing = False

        with shutils.input_file(self.rc) as file:
            for i, line in enumerate(file):
                m = re.match(_export_path_pattern, line.rstrip())
                if m is not None:
                    last_export_path_no = i
                    # extract paths in PATH
                    paths_in_path = [
                        path
                        for path in (
                            *m.group(1).split(":"),
                            "$PATH",
                            *m.group(2).split(":"),
                        )
                        if path
                    ]
                    # if already in PATH, break
                    if self.path in paths_in_path:
                        existing = True
                        break

        if existing:
            self.appended = False

        else:
            with shutils.input_file(self.rc, inplace=True) as file:
                for i, line in enumerate(file):
                    # if no export path line, prepend to the file
                    if last_export_path_no == -1:
                        if i == 0:
                            sys.stdout.write(f'export PATH="$PATH:{self.path}"\n')
                        sys.stdout.write(line)

                    # if the last export path line, append to the line
                    elif last_export_path_no == i:
                        dollar_path_at_left = paths_in_path.index("$PATH") == 0
                        if len(line) + len(self.path) + 1 >= 80:
                            # if the line is too long, append after the last export line
                            paths_in_path = ["$PATH"]
                            line = line if line.endswith("\n") else f"{line}\n"
                            sys.stdout.write(f"{line}")

                        paths_in_path.insert(
                            len(paths_in_path) if dollar_path_at_left else -1, self.path
                        )
                        sys.stdout.write(f'export PATH="{":".join(paths_in_path)}"\n')

                    # no touch other lines
                    else:
                        sys.stdout.write(line)

            self.appended = True

        self.ret = self._success_result()
        return self.ret

    def _undo(self):
        with shutils.input_file(self.rc, inplace=True) as file:
            for line in file:
                m = re.match(_export_path_pattern, line.rstrip())
                if m is not None:
                    # extract paths in PATH
                    paths_in_path = [
                        *m.group(1).split(":"),
                        "$PATH",
                        *m.group(2).split(":"),
                    ]

                    # if in PATH, remove it and write back
                    if self.path in paths_in_path:
                        paths_in_path.remove(self.path)
                        sys.stdout.write(f'export PATH="{":".join(paths_in_path)}"\n')

                    # no touch other lines
                    else:
                        sys.stdout.write(line)

        self.appended = None
        self.ret = None

    def spec_tuple(self):
        return self.path, self.rc

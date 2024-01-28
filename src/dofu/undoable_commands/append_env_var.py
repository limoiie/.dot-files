import dataclasses
import re
import sys
import typing as t

from dofu import shutils
from dofu.undoable_command import ExecutionResult, UndoableCommand

_export_path_pattern = re.compile(r"export\s([a-zA-Z_][a-zA-Z0-9_]*)=(.*)")


@dataclasses.dataclass
class UCAppendEnvVar(UndoableCommand):
    varname: str
    value: str
    rc: str
    origin_value: t.Optional[str] = None
    ret: t.Optional[ExecutionResult] = None

    @staticmethod
    def make_multiple_rcs(varname: str, value: str, *rcs: str):
        return [UCAppendEnvVar(varname=varname, value=value, rc=rc) for rc in rcs]

    def cmdline(self) -> str:
        return f"echo 'export {self.varname}={self.value} >> {self.rc}'"

    def _exec(self):
        last_export_no = -1
        varname, value = None, None
        already_set = False

        with shutils.input_file(self.rc) as file:
            for i, line in enumerate(file):
                m = re.match(_export_path_pattern, line.rstrip())
                if m is not None:
                    last_export_no = i
                    varname, value = m.groups()
                    # if already set, break
                    if self.varname == varname:
                        already_set = value == self.value
                        break

        if already_set:
            self.origin_value = None

        else:
            with shutils.input_file(self.rc, inplace=True) as file:
                for i, line in enumerate(file):
                    # if no export line, prepend to the file
                    if last_export_no == -1:
                        if i == 0:
                            sys.stdout.write(f"export {self.varname}={self.value}\n")
                        sys.stdout.write(line)

                    # if the export line, change its value
                    elif last_export_no == i:
                        if varname != self.varname:
                            # if export other var, keep it
                            sys.stdout.write(
                                line if line.endswith("\n") else line + "\n"
                            )

                        sys.stdout.write(f"export {self.varname}={self.value}\n")

                    # no touch other lines
                    else:
                        sys.stdout.write(line)

            self.origin_value = value

        self.ret = self._success_result()
        return self.ret

    def _undo(self):
        if self.origin_value is None:
            pass

        else:
            is_reset = False
            with shutils.input_file(self.rc, inplace=True) as file:
                for line in file:
                    if not is_reset:
                        m = re.match(_export_path_pattern, line.rstrip())
                        # if export self.varname, reset its value
                        if m is not None and m.group(1) == self.varname:
                            is_reset = True
                            sys.stdout.write(
                                f"export {self.varname}={self.origin_value}\n"
                            )
                            continue

                    # no touch other lines
                    sys.stdout.write(line)

        self.origin_value = None
        self.ret = None

    def spec_tuple(self):
        return self.varname, self.value, self.rc

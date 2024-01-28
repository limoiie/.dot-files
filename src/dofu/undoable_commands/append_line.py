import dataclasses
import re
import sys
import typing as t

from dofu import shutils
from dofu.undoable_command import ExecutionResult, UndoableCommand


@dataclasses.dataclass
class UCAppendLine(UndoableCommand):
    path: str
    pattern: str
    repl: str
    replaced_line: t.Optional[str] = None
    ret: t.Optional[ExecutionResult] = None

    @staticmethod
    def make_source_line(
        path: str, pattern: str, file_to_source: str, check_exists: bool = True
    ):
        repl = f'source "{file_to_source}"'
        if check_exists:
            repl = f'[ -f "{file_to_source}" ] && {repl}'
        return UCAppendLine(path=path, pattern=pattern, repl=repl)

    def cmdline(self) -> str:
        return f"sed -i.dofu.bak 's/{self.pattern}/{self.repl}/g' {self.path}"

    def _exec(self):
        replaced_line = None
        pattern = re.compile(self.pattern)
        with shutils.input_file(self.path, inplace=True) as file:
            for line in file:
                # replace the first line that matches the pattern
                if replaced_line is None and re.search(pattern, line):
                    replaced_line = line
                    new_line = self.repl.rstrip("\n")
                    line = (new_line + "\n") if line.endswith("\n") else new_line
                sys.stdout.write(line)

        # if no line was replaced, append the line at the end of the file
        if replaced_line is None:
            # append the line at the end of the file
            shutils.check_call(f"echo '{self.repl}' >> {self.path}")
            replaced_line = ""

        self.replaced_line = replaced_line
        self.ret = self._success_result()
        return self.ret

    def _undo(self):
        with shutils.input_file(self.path, inplace=True) as file:
            for line in file:
                if line.startswith(self.repl):
                    line = self.replaced_line
                sys.stdout.write(line)

    def spec_tuple(self):
        return self.path, self.pattern, self.repl

import dataclasses
import enum


class Strategy(enum.Enum):
    INTERACTIVE = 0
    """
    Ask the user what to do.
    """

    OVERWRITE = 1
    """
    Solve the problem by overwriting in force.
    """

    NON_INTRUSIVE = 2
    """
    Non-intrusively try to solve the problem.
    """

    CANCEL = 3
    """
    Cancel the operation.
    """

    @staticmethod
    def from_flags(*, interactive: bool, overwrite: bool, backup: bool, cancel: bool):
        assert (
            interactive + overwrite + backup + cancel == 1
        ), f"Choose exactly one strategy from {','.join(Strategy.all_names())}"

        if interactive:
            return Strategy.INTERACTIVE
        elif overwrite:
            return Strategy.OVERWRITE
        elif backup:
            return Strategy.NON_INTRUSIVE
        elif cancel:
            return Strategy.CANCEL

    @staticmethod
    def all_names():
        return [
            Strategy.INTERACTIVE.name,
            Strategy.OVERWRITE.name,
            Strategy.NON_INTRUSIVE.name,
            Strategy.CANCEL.name,
        ]

    @staticmethod
    def all_decidable_names():
        return [
            Strategy.OVERWRITE.name,
            Strategy.NON_INTRUSIVE.name,
            Strategy.CANCEL.name,
        ]


@dataclasses.dataclass
class Options:
    dry_run: bool
    """
    If True, don't execute the commands, just print them.
    """

    strategy: Strategy
    """
    Strategy to use whenever meeting a destructive command.

    The user will be prompted to confirm their advice 
    when executing a destructive command.
    For instance, 
    if the command is to move a file to a destination that already exists,
    a confirmation will appear asking 
    whether to overwrite the destination, create a backup, or cancel the operation.
    """

    @staticmethod
    def instance():
        return _options


_options: Options = Options(
    dry_run=False,
    strategy=Strategy.CANCEL,
)

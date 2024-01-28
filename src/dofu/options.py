import dataclasses
import enum


class Strategy(enum.Enum):
    ASK = 0
    """
    Ask the user what to do.
    """

    FORCE = 1
    """
    Solve the problem by overwriting in force.
    """

    AUTO = 2
    """
    Non-intrusively try to solve the problem.
    """

    QUIT = 3
    """
    Cancel the operation.
    """

    @staticmethod
    def from_name(name: str):
        return Strategy[name.upper()]

    @staticmethod
    def all_names():
        return [
            Strategy.ASK.name,
            Strategy.FORCE.name,
            Strategy.AUTO.name,
            Strategy.QUIT.name,
        ]

    @staticmethod
    def all_decidable_names():
        return [
            Strategy.FORCE.name,
            Strategy.AUTO.name,
            Strategy.QUIT.name,
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
    strategy=Strategy.ASK,
)

import logging
import typing
from logging import LogRecord

from rich.logging import RichHandler
from rich.text import Text


class LogHandler(RichHandler):
    _level_styles = dict(
        DEBU="bold #6061f7",  # blue
        INFO="bold #69fedb",  # cyan
        WARN="bold #d8fe85",  # green
        ERRO="bold #fe668a",  # red
        FATA="bold #b35edc",  # purple
    )

    def get_level_text(self, record: LogRecord) -> Text:
        """
        Get the level name from the record.

        :param record: LogRecord instance.
        :returns: A tuple of the style and level name.
        """
        level_name = record.levelname
        level_text = Text.styled(
            level_name.ljust(4), style=self._level_styles[level_name]
        )
        return level_text


def init(
    loglevel: typing.Literal["debug", "info", "warn", "error", "fatal"] = None,
):
    """
    Initialize logging.
    """

    logging.addLevelName(logging.DEBUG, f"DEBU")
    logging.addLevelName(logging.INFO, f"INFO")
    logging.addLevelName(logging.WARNING, f"WARN")
    logging.addLevelName(logging.ERROR, f"ERRO")
    logging.addLevelName(logging.FATAL, f"FATA")

    logging.basicConfig(
        format=f"[dim]%(name)s[/] %(message)s",
        datefmt="%H:%M",
        level=getattr(logging, (loglevel or "info").upper(), logging.INFO),
        handlers=[
            LogHandler(rich_tracebacks=True, markup=True),
        ],
    )

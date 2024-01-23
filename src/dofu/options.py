import dataclasses


@dataclasses.dataclass
class Options:
    dry_run: bool

    @staticmethod
    def instance():
        return _options


_options: Options = Options(
    dry_run=False,
)

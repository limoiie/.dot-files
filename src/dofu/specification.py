import dataclasses


@dataclasses.dataclass
class PackageSpecification:
    package: str
    """
    The package name.
    """

    version: str = "latest"
    """
    The version of the package.
    """

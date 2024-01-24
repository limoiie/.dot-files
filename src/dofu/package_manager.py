import abc
import dataclasses

from dofu import shutils


@dataclasses.dataclass
class PackageManager(abc.ABC):
    @abc.abstractmethod
    def install(self, package) -> bool:
        pass

    @abc.abstractmethod
    def uninstall(self, package) -> bool:
        pass

    @abc.abstractmethod
    def update(self, package):
        pass

    @abc.abstractmethod
    def is_available(self) -> bool:
        return False


@dataclasses.dataclass
class CurlShPackageManager(PackageManager):
    install_cmd: str
    """
    Shell script to install the package manager.
    """

    uninstall_cmd: str
    """
    Shell script to uninstall the package manager.
    """

    update_cmd: str = None
    """
    Shell script to update the package manager.
    """

    def __post_init__(self):
        if self.update_cmd is None:
            self.update_cmd = self.install_cmd

    def install(self, package):
        return shutils.call(self.install_cmd) == 0

    def uninstall(self, package):
        return shutils.call(self.uninstall_cmd) == 0

    def update(self, package):
        return shutils.call(self.update_cmd) == 0

    def is_available(self) -> bool:
        return shutils.do_commands_exist("curl", "sh")


@dataclasses.dataclass
class AptPackageManager(PackageManager):
    def install(self, package):
        return shutils.call(f"sudo apt install -y {package}") == 0

    def uninstall(self, package):
        return shutils.call(f"sudo apt uninstall -y {package}") == 0

    def update(self, package):
        return shutils.call(f"sudo apt upgrade -y {package}") == 0

    def is_available(self) -> bool:
        return shutils.do_commands_exist("apt")


@dataclasses.dataclass
class CargoPackageManager(PackageManager):
    def install(self, package):
        return shutils.call(f"cargo install {package}") == 0

    def uninstall(self, package):
        return shutils.call(f"cargo uninstall {package}") == 0

    def update(self, package):
        return shutils.call(f"cargo update --package {package}") == 0

    def is_available(self) -> bool:
        return shutils.do_commands_exist("cargo")


@dataclasses.dataclass
class BobNvimPackageManager(PackageManager):
    def install(self, package):
        return shutils.call(f"bob use latest") == 0

    def uninstall(self, package):
        return shutils.call(f"bob uninstall latest") == 0

    def update(self, package):
        return shutils.call(f"bob use latest") == 0

    def is_available(self) -> bool:
        return shutils.do_commands_exist("bob")

import abc
import dataclasses
import subprocess

from dofu import utils


@dataclasses.dataclass
class PackageManager(abc.ABC):
    @abc.abstractmethod
    def install(self, package) -> bool:
        pass

    @abc.abstractmethod
    def uninstall(self, package) -> bool:
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

    def install(self, package):
        return subprocess.call(self.install_cmd, shell=True) == 0

    def uninstall(self, package):
        return subprocess.call(self.uninstall_cmd, shell=True) == 0

    def is_available(self) -> bool:
        return utils.do_commands_exist("curl", "sh")


@dataclasses.dataclass
class AptPackageManager(PackageManager):
    def install(self, package):
        return subprocess.call(f"sudo apt install -y {package}", shell=True) == 0

    def uninstall(self, package):
        return subprocess.call(f"sudo apt uninstall -y {package}", shell=True) == 0

    def is_available(self) -> bool:
        return utils.do_commands_exist("apt")


@dataclasses.dataclass
class CargoPackageManager(PackageManager):
    def install(self, package):
        return subprocess.call(f"cargo install {package}", shell=True) == 0

    def uninstall(self, package):
        return subprocess.call(f"cargo uninstall {package}", shell=True) == 0

    def is_available(self) -> bool:
        return utils.do_commands_exist("cargo")


@dataclasses.dataclass
class BobNvimPackageManager(PackageManager):
    def install(self, package):
        return subprocess.call(f"bob use latest", shell=True) == 0

    def uninstall(self, package):
        return subprocess.call(f"bob uninstall latest", shell=True) == 0

    def is_available(self) -> bool:
        return utils.do_commands_exist("bob")

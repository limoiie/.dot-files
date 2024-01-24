import dataclasses

from dofu import shutils
from dofu.package_manager import PackageManager


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

    def install(self, spec):
        return shutils.call(self.install_cmd) == 0

    def uninstall(self, spec):
        return shutils.call(self.uninstall_cmd) == 0

    def update(self, spec):
        return shutils.call(self.update_cmd) == 0

    def is_available(self) -> bool:
        return shutils.do_commands_exist("curl", "sh")

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
        shutils.check_call(self.install_cmd.format(version=spec.version))

    def uninstall(self, spec):
        shutils.check_call(self.uninstall_cmd.format(version=spec.version))

    def update(self, spec):
        shutils.check_call(self.update_cmd)

    def is_available(self) -> bool:
        return shutils.do_commands_exist("curl", "sh")

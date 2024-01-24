import dataclasses

from dofu import shutils
from dofu.package_manager import PackageManager


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

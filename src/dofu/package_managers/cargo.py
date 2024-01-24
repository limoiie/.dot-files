import dataclasses

from dofu import shutils
from dofu.package_manager import PackageManager


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

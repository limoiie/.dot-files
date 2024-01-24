import dataclasses

from dofu import shutils
from dofu.package_manager import PackageManager


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

import dataclasses

from dofu import shutils
from dofu.package_manager import PackageManager


@dataclasses.dataclass
class BobNvimPackageManager(PackageManager):
    def install(self, spec):
        shutils.check_call(f"bob use {spec.version}")

    def uninstall(self, spec):
        shutils.check_call(f"bob uninstall {spec.version}")

    def update(self, spec):
        return self.install(spec)

    def is_available(self) -> bool:
        return shutils.do_commands_exist("bob")

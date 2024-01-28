import dataclasses

from dofu import shutils
from dofu.package_manager import PackageManager


@dataclasses.dataclass
class PacmanPackageManager(PackageManager):
    def install(self, spec):
        shutils.check_call(f"sudo pacman -S {spec.package}")

    def uninstall(self, spec):
        shutils.check_call(f"sudo pacman -R {spec.package}")

    def update(self, spec):
        self.install(spec)

    def is_available(self) -> bool:
        return shutils.do_commands_exist("pacman")

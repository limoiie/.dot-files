import dataclasses

from dofu import shutils
from dofu.package_manager import PackageManager


@dataclasses.dataclass
class BrewPackageManager(PackageManager):
    def install(self, spec):
        if not spec.version or spec.version == "latest":
            shutils.check_call(f"brew install {spec.package}")
            return
        shutils.check_call(f"brew install {spec.package}@{spec.version}")

    def uninstall(self, spec):
        if not spec.version or spec.version == "latest":
            shutils.check_call(f"brew uninstall {spec.package}")
            return
        shutils.check_call(f"brew uninstall {spec.package}@{spec.version}")

    def update(self, spec):
        if not spec.version or spec.version == "latest":
            shutils.check_call(f"brew upgrade {spec.package}")
            return
        shutils.check_call(f"brew upgrade {spec.package}@{spec.version}")

    def is_available(self) -> bool:
        return shutils.do_commands_exist("brew")

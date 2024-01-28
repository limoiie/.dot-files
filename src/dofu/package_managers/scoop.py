import dataclasses

from dofu import shutils
from dofu.package_manager import PackageManager


@dataclasses.dataclass
class ScoopPackageManager(PackageManager):
    def install(self, spec):
        if not spec.version or spec.version != "latest":
            shutils.check_call(f"scoop install {spec.package}@{spec.version}")
            return
        shutils.check_call(f"scoop install {spec.package}")

    def uninstall(self, spec):
        if not spec.version or spec.version != "latest":
            shutils.check_call(f"scoop uninstall {spec.package}@{spec.version}")
            return
        shutils.check_call(f"scoop uninstall {spec.package}")

    def update(self, spec):
        if not spec.version or spec.version != "latest":
            shutils.check_call(f"scoop update {spec.package}@{spec.version}")
            return
        shutils.check_call(f"scoop update {spec.package}")

    def is_available(self) -> bool:
        return shutils.do_commands_exist("scoop")

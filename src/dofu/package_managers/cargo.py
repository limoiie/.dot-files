import dataclasses

from dofu import shutils
from dofu.package_manager import PackageManager


@dataclasses.dataclass
class CargoPackageManager(PackageManager):
    def install(self, spec):
        if not spec.version or spec.version == "latest":
            shutils.check_call(f"cargo install {spec.package}")
        shutils.check_call(f"cargo install --version {spec.version} {spec.package}")

    def uninstall(self, spec):
        shutils.check_call(f"cargo uninstall --package {spec.package}")

    def update(self, spec):
        return self.install(spec)

    def is_available(self) -> bool:
        return shutils.do_commands_exist("cargo")

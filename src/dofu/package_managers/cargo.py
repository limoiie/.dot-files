import dataclasses

from dofu import shutils
from dofu.package_manager import PackageManager


@dataclasses.dataclass
class CargoPackageManager(PackageManager):
    def install(self, spec):
        if not spec.version or spec.version == "latest":
            return shutils.call(f"cargo install {spec.package}") == 0
        return (
            shutils.call(f"cargo install --version {spec.version} {spec.package}") == 0
        )

    def uninstall(self, spec):
        return shutils.call(f"cargo uninstall --package {spec.package}") == 0

    def update(self, spec):
        return self.install(spec)

    def is_available(self) -> bool:
        return shutils.do_commands_exist("cargo")

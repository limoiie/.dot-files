import dataclasses

from dofu import shutils
from dofu.package_manager import PackageManager


@dataclasses.dataclass
class AptPackageManager(PackageManager):
    def install(self, spec):
        if not spec.version or spec.version == "latest":
            return shutils.call(f"sudo apt install -y {spec.package}") == 0
        return shutils.call(f"sudo apt install -y {spec.package}={spec.version}") == 0

    def uninstall(self, spec):
        return shutils.call(f"sudo apt uninstall -y {spec.package}") == 0

    def update(self, spec):
        return self.install(spec)

    def is_available(self) -> bool:
        return shutils.do_commands_exist("apt")

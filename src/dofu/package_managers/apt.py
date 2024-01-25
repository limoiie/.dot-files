import dataclasses

from dofu import shutils
from dofu.package_manager import PackageManager


@dataclasses.dataclass
class AptPackageManager(PackageManager):
    def install(self, spec):
        if not spec.version or spec.version == "latest":
            shutils.check_call(f"sudo apt install -y {spec.package}")
        shutils.check_call(f"sudo apt install -y {spec.package}={spec.version}")

    def uninstall(self, spec):
        shutils.check_call(f"sudo apt uninstall -y {spec.package}")

    def update(self, spec):
        self.install(spec)

    def is_available(self) -> bool:
        return shutils.do_commands_exist("apt")

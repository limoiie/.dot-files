import dataclasses

from dofu import shutils
from dofu.package_manager import PackageManager


@dataclasses.dataclass
class ChocolateyPackageManager(PackageManager):
    def install(self, spec):
        if not spec.version or spec.version != "latest":
            shutils.check_call(f"choco install {spec.package} --version {spec.version}")
        shutils.check_call(f"choco install {spec.package}")

    def uninstall(self, spec):
        if not spec.version or spec.version != "latest":
            shutils.check_call(
                f"choco uninstall {spec.package} --version {spec.version}"
            )
        shutils.check_call(f"choco uninstall {spec.package}")

    def update(self, spec):
        self.install(spec)

    def is_available(self) -> bool:
        return shutils.do_commands_exist("choco")

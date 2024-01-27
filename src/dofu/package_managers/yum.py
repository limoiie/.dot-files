import dataclasses

from dofu import shutils
from dofu.package_manager import PackageManager


@dataclasses.dataclass
class YumPackageManager(PackageManager):
    def install(self, spec):
        if not spec.version or spec.version == "latest":
            shutils.check_call(f"sudo yum install -y {spec.package}")
        shutils.check_call(f"sudo yum install {spec.package}-{spec.version}")

    def uninstall(self, spec):
        if not spec.version or spec.version == "latest":
            shutils.check_call(f"sudo yum remove {spec.package}")
        shutils.check_call(f"sudo yum remove {spec.package}-{spec.version}")

    def update(self, spec):
        self.install(spec)

    def is_available(self) -> bool:
        return shutils.do_commands_exist("yum")

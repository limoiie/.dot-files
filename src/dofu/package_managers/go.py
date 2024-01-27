import dataclasses

from dofu import shutils
from dofu.package_manager import PackageManager


@dataclasses.dataclass
class GoPackageManager(PackageManager):
    def install(self, spec):
        shutils.check_call(f"go install {spec.version}@{spec.package}")

    def uninstall(self, spec):
        # TODO: no uninstall command for go
        pass

    def update(self, spec):
        return self.install(spec)

    def is_available(self) -> bool:
        return shutils.do_commands_exist("go")

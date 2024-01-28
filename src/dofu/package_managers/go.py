import dataclasses
import logging

from dofu import shutils
from dofu.package_manager import PackageManager

_logger = logging.getLogger(__name__)


@dataclasses.dataclass
class GoPackageManager(PackageManager):
    def install(self, spec):
        shutils.check_call(f"go install {spec.package}@{spec.version}")

    def uninstall(self, spec):
        _logger.warning("Uninstalling Go packages is not supported")

    def update(self, spec):
        return self.install(spec)

    def is_available(self) -> bool:
        return shutils.do_commands_exist("go")

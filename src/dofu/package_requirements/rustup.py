import dataclasses

from dofu import package_managers as pms, platform as pf
from dofu.requirement import PackageRequirement


@dataclasses.dataclass
class PRRustup(PackageRequirement):
    _pkg_manager_candidates = {
        pf.LINUX: pms.CurlShPackageManager(
            "curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh",
            "rustup self uninstall",
        ),
    }

    package: str = "rustup"
    version: str = "latest"
    command: str = "rustup"

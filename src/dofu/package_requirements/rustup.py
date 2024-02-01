import dataclasses

from dofu import package_managers as pms, platform as pf, specification as sp
from dofu.requirement import PackageRequirement


@dataclasses.dataclass
class PRRustup(PackageRequirement):
    _pkg_manager_candidates = {
        pf.LINUX: pms.CurlShPackageManager(
            "curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh",
            "rustup self uninstall",
        ),
    }

    spec: sp.PackageSpecification = dataclasses.field(
        default_factory=lambda: sp.PackageSpecification(
            package="rustup",
            version="latest",
        )
    )
    command: str = "rustup"

import dataclasses

from dofu import package_managers as pms, platform as pf, specification as sp
from dofu.requirement import PackageRequirement


@dataclasses.dataclass
class PRNeovim(PackageRequirement):
    _pkg_manager_candidates = {
        pf.ANY: pms.BobNvimPackageManager(),
    }

    spec: sp.PackageSpecification = sp.PackageSpecification(
        package="neovim",
        version="latest",
    )
    command: str = "nvim"

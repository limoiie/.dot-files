import dataclasses

from dofu import package_managers as pms, platform as pf, specification as sp
from dofu.requirement import PackageRequirement


@dataclasses.dataclass
class PRBob(PackageRequirement):
    _pkg_manager_candidates = {
        pf.ANY: pms.CargoPackageManager(),
    }

    spec: sp.PackageSpecification = sp.PackageSpecification(
        package="bob-nvim",
        version="latest",
    )
    command: str = "bob"

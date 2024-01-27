import dataclasses

from dofu import package_managers as pms, platform as pf
from dofu.requirement import PackageRequirement


@dataclasses.dataclass
class PRCargoCrate(PackageRequirement):
    _pkg_manager_candidates = {
        pf.ANY: pms.CargoPackageManager(),
    }

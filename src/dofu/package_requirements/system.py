import dataclasses

from dofu import package_managers as pms, platform as pf
from dofu.requirement import PackageRequirement


@dataclasses.dataclass
class PRSystem(PackageRequirement):
    _pkg_manager_candidates = {
        pf.MACOS: pms.BrewPackageManager(),
        pf.LINUX: [
            pms.AptPackageManager(),
            pms.PacmanPackageManager(),
            pms.YumPackageManager(),
        ],
        pf.WINDOWS: [
            pms.ChocolateyPackageManager(),
            pms.ScoopPackageManager(),
        ],
    }

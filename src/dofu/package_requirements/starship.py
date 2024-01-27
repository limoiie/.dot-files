import dataclasses

from dofu import package_managers as pms, platform as pf, specification as sp
from dofu.requirement import PackageRequirement


@dataclasses.dataclass
class PRStarship(PackageRequirement):
    _pkg_manager_candidates = {
        pf.ANY: pms.CargoPackageManager(),
        pf.LINUX: pms.CurlShPackageManager(
            "curl --proto '=https' --tlsv1.2 -sSf https://starship.rs/install.sh | sh",
            "sh -c 'rm \"$(command -v 'starship')\"'",
        ),
    }

    spec: sp.PackageSpecification = sp.PackageSpecification(
        package="starship",
        version="latest",
    )
    command: str = "starship"

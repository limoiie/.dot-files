import dataclasses

from dofu import package_managers as pms, platform as pf, specification as sp
from dofu.requirement import PackageRequirement


@dataclasses.dataclass
class PRGolang(PackageRequirement):
    _pkg_manager_candidates = {
        pf.LINUX: pms.CurlShPackageManager(
            install_cmd="curl -sSL https://golang.org/dl/go{version}.linux-amd64.tar.gz | sudo tar -C /usr/local -xzf -",
            uninstall_cmd="sudo rm -rf /usr/local/go",
            update_cmd="echo 'No update command available.'",
        ),
        pf.MACOS: pms.CurlShPackageManager(
            install_cmd="curl -sSL https://golang.org/dl/go{version}.darwin-amd64.tar.gz | sudo tar -C /usr/local -xzf -",
            uninstall_cmd="sudo rm -rf /usr/local/go",
            update_cmd="echo 'No update command available.'",
        ),
    }

    spec: sp.PackageSpecification = dataclasses.field(
        default_factory=lambda: sp.PackageSpecification(
            package="go",
            version="1.21.6",
        )
    )
    command: str = "go"

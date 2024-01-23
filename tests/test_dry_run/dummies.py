import dataclasses
import typing as t

from dofu import (
    module,
    package_manager as pm,
    platform as pf,
    requirements as req,
    shutils,
    undoable_command as uc,
)
from .conftest import under_temp_workspace


@dataclasses.dataclass
class DummyWindowsPackageManager(pm.PackageManager):
    def install(self, package):
        return shutils.call(f'echo "pm-dummy install {package}"', shell=True) == 0

    def uninstall(self, package):
        return shutils.call(f'echo "pm-dummy uninstall {package}"', shell=True) == 0

    def is_available(self) -> bool:
        return shutils.do_commands_exist("echo")


@dataclasses.dataclass
class DummyUnixPackageManager(pm.PackageManager):
    def install(self, package):
        return shutils.call(f'echo "pm-dummy install {package}"', shell=True) == 0

    def uninstall(self, package):
        return shutils.call(f'echo "pm-dummy uninstall {package}"', shell=True) == 0

    def is_available(self) -> bool:
        return shutils.do_commands_exist("echo")


@dataclasses.dataclass
class DummyPackageRequirement(req.PackageRequirement):
    _pkg_manager_candidates = {
        pf.WINDOWS: DummyWindowsPackageManager(),
        pf.LINUX: DummyUnixPackageManager(),
        pf.MACOS: DummyUnixPackageManager(),
    }

    package: str = "dummy-pkg"
    version: str = "latest"
    command: str = "dummy-cmd"


@dataclasses.dataclass
class UCDummy(uc.UndoableCommand):
    content: str
    ret: t.Optional[uc.ExecutionResult] = None

    def exec(self) -> uc.ExecutionResult:
        cmdline = f'echo "uc-dummy exec {self.content}"'
        shutils.call(cmdline, shell=True)
        self.ret = uc.ExecutionResult(
            cmdline=cmdline, retcode=0, stdout=None, stderr=None
        )
        return self.ret

    def undo(self):
        shutils.call('echo "dummy undo"', shell=True)
        self.ret = None

    def spec_tuple(self):
        return (self.content,)


@module.Module.module("dummy", requires=[])
class DummyModule(module.Module):
    _package_requirements = [
        DummyPackageRequirement(),
    ]

    _git_repo_requirements = [
        req.GitRepoRequirement(
            repo="https://github.com/sarcasticadmin/empty-repo",
            path=under_temp_workspace("dummy-repo"),
        ),
    ]

    _config_steps = [
        UCDummy(content="dummy-content"),
    ]

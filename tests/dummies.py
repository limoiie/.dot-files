import dataclasses
import typing as t

from dofu import (
    package_manager as pm,
    platform as pf,
    requirement as req,
    shutils,
    specification as sp,
    undoable_command as uc,
)


@dataclasses.dataclass
class DummyWindowsPackageManager(pm.PackageManager):
    def install(self, spec):
        shutils.check_call(f'echo "pm-dummy install {spec.package}"')

    def uninstall(self, spec):
        shutils.check_call(f'echo "pm-dummy uninstall {spec.package}"')

    def update(self, spec):
        shutils.check_call(f'echo "pm-dummy update {spec.package}"')

    def is_available(self) -> bool:
        return shutils.do_commands_exist("echo")


@dataclasses.dataclass
class DummyUnixPackageManager(pm.PackageManager):
    def install(self, spec):
        shutils.check_call(f'echo "pm-dummy install {spec.package}"')

    def uninstall(self, spec):
        shutils.check_call(f'echo "pm-dummy uninstall {spec.package}"')

    def update(self, spec):
        shutils.check_call(f'echo "pm-dummy update {spec.package}"')

    def is_available(self) -> bool:
        return shutils.do_commands_exist("echo")


@dataclasses.dataclass
class DummyPackageRequirement(req.PackageRequirement):
    _pkg_manager_candidates = {
        pf.WINDOWS: DummyWindowsPackageManager(),
        pf.LINUX: DummyUnixPackageManager(),
        pf.MACOS: DummyUnixPackageManager(),
    }

    spec: sp.PackageSpecification = sp.PackageSpecification(
        package="dummy-pkg",
        version="latest",
    )
    command: str = "dummy-cmd"


@dataclasses.dataclass
class UCDummy(uc.UndoableCommand):
    content: str
    ret: t.Optional[uc.ExecutionResult] = None

    def cmdline(self) -> str:
        return f'echo "uc-dummy exec {self.content}"'

    def _exec(self) -> uc.ExecutionResult:
        shutils.call(self.cmdline())
        self.ret = self._success_result()
        return self.ret

    def _undo(self):
        shutils.call('echo "dummy undo"')
        self.ret = None

    def spec_tuple(self):
        return (self.content,)

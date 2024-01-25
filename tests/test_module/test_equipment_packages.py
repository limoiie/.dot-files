import dataclasses
import typing as t

import pytest

from dofu import (
    equipment as eqp,
    module,
    package_manager as pm,
    platform as pf,
    requirement as req,
    specification as sp,
)


@dataclasses.dataclass
class ExecEnv:
    """
    The execution environment for testing.

    This class is used to mock the execution environment.
    Any changes to the environment can be tracked by this class.
    """

    commands: t.List[str] = dataclasses.field(default_factory=list)
    package_managers: t.List[pm.PackageManager] = dataclasses.field(
        default_factory=list
    )

    def install_package(self, package_manager, spec):
        pass

    def uninstall_package(self, package_manager, spec):
        pass

    def update_package(self, _package_manager, _spec):
        pass

    def is_available(self, package_manager):
        return package_manager in self.package_managers


mock_env: ExecEnv = None
"""
The mock execution environment used by the test classes inner this file.
"""


@dataclasses.dataclass
class MockPackageManager(pm.PackageManager):
    """
    A mock package manager for testing,
    should be inherited by other mock package managers.

    By inheriting this class,
    all the behaviours of the mock package managers can be tracked by the mock_env.
    """

    def install(self, spec: sp.PackageSpecification) -> bool:
        return mock_env.install_package(self, spec)

    def uninstall(self, spec: sp.PackageSpecification) -> bool:
        return mock_env.uninstall_package(self, spec)

    def update(self, spec: sp.PackageSpecification) -> bool:
        return mock_env.update_package(self, spec)

    def is_available(self) -> bool:
        return mock_env.is_available(self)


@dataclasses.dataclass
class MockPackageRequirement(req.PackageRequirement):
    """
    A mock package requirement for testing,
    should be inherited by other mock package requirements.

    By inheriting this class,
    all the behaviours of the mock package requirements can be tracked by the mock_env.
    """

    def install(self):
        package_manager = super().install()
        if package_manager is not None:
            mock_env.commands.append(self.command)
        return package_manager

    def uninstall(self, package_manager):
        package_manager = super().uninstall(package_manager)
        if package_manager:
            mock_env.commands.remove(self.command)
        return package_manager

    def update(self, pkg_manager):
        package_manager = super().update(pkg_manager)
        if package_manager:
            mock_env.commands.append(self.command)
        return package_manager

    def is_satisfied(self):
        return self.command in mock_env.commands


@dataclasses.dataclass
class TestAvailPackageManager(MockPackageManager):
    pass


@dataclasses.dataclass
class TestOnePackageRequirement(MockPackageRequirement):
    _pkg_manager_candidates = {
        pf.ANY: TestAvailPackageManager(),
    }

    spec: sp.PackageSpecification = sp.PackageSpecification("test-one-pkg")
    command: str = "test-one-cmd"


@dataclasses.dataclass
class TestOtherPackageRequirement(MockPackageRequirement):
    _pkg_manager_candidates = {
        pf.ANY: TestAvailPackageManager(),
    }

    spec: sp.PackageSpecification = sp.PackageSpecification("test-other-pkg")
    command: str = "test-other-cmd"


class TestEquipmentSyncPackages:
    @pytest.fixture(scope="function", autouse=True)
    def graph(self, registration_preserver):
        """
        This fixture is responsible to provide a clean graph for each test.

        Any registration happened during the test will be removed after the test.
        """
        yield registration_preserver

    @pytest.fixture(scope="function")
    def clean_env(self):
        global mock_env
        mock_env = ExecEnv()
        yield mock_env
        mock_env = None

    @classmethod
    def test_sync_with_clean_env(cls, clean_env: ExecEnv):
        """
        Test that the package requirement can be synchronized correctly
        with respect to the changes in the _package_requirements field.

        The default environment is clean,
        which means that no package is installed by any one.
        """
        one_pkg_requirement = TestOnePackageRequirement()

        @module.Module.module("test-one-module")
        class TestOneModule(module.Module):
            _package_requirements = [
                one_pkg_requirement,
            ]
            _gitrepo_requirements = []
            _command_requirements = []

        # install test-one-module
        mngr = eqp.ModuleEquipmentManager()
        mngr.sync(["test-one-module"])
        meta = mngr.meta["test-one-module"]

        # check that the package requirement is installed
        installation = get_installation(meta, one_pkg_requirement)
        assert installation is not None and installation.used_existing == False
        assert one_pkg_requirement.command in clean_env.commands

        other_pkg_requirement = TestOtherPackageRequirement()

        # mick the update onto the package requirements
        # add one more package requirement to test-one-module
        TestOneModule._package_requirements.append(other_pkg_requirement)
        mngr.sync(["test-one-module"])

        # check that the package requirement is installed
        installation = get_installation(meta, one_pkg_requirement)
        assert installation is not None and installation.used_existing == False
        installation = get_installation(meta, other_pkg_requirement)
        assert installation is not None and installation.used_existing == False
        assert one_pkg_requirement.command in clean_env.commands
        assert other_pkg_requirement.command in clean_env.commands
        assert meta.status == eqp.ModuleEquipmentStatus.INSTALLED

        # mick the update onto the package requirements
        # remove the package requirement from test-one-module
        TestOneModule._package_requirements.pop(0)
        mngr.sync(["test-one-module"])

        # check that the one-package-requirement is uninstalled
        installation = get_installation(meta, one_pkg_requirement)
        assert installation is None
        installation = get_installation(meta, other_pkg_requirement)
        assert installation is not None and installation.used_existing == False
        assert one_pkg_requirement.command not in clean_env.commands
        assert other_pkg_requirement.command in clean_env.commands
        assert meta.status == eqp.ModuleEquipmentStatus.INSTALLED

        # mick the update onto the package requirements
        # replace the package requirement from test-one-module
        TestOneModule._package_requirements.pop(0)
        TestOneModule._package_requirements.append(TestOnePackageRequirement())
        mngr.sync(["test-one-module"])

        # check that the other-package-requirement is replaced by one-package
        installation = get_installation(meta, one_pkg_requirement)
        assert installation is not None and installation.used_existing == False
        installation = get_installation(meta, other_pkg_requirement)
        assert installation is None
        assert one_pkg_requirement.command in clean_env.commands
        assert other_pkg_requirement.command not in clean_env.commands
        assert meta.status == eqp.ModuleEquipmentStatus.INSTALLED

    @pytest.fixture(scope="function")
    def partial_ready_env(self):
        global mock_env
        mock_env = ExecEnv(commands=["test-one-cmd"])
        yield mock_env
        mock_env = None

    @classmethod
    def test_sync_with_partial_ready_env(cls, partial_ready_env: ExecEnv):
        """
        Test that the package requirement can be synchronized correctly
        with respect to the changes in the _package_requirements field.

        The partial ready environment is partially ready,
        that is, some commands have been installed by others before running dofu.
        """
        one_pkg_requirement = TestOnePackageRequirement()

        @module.Module.module("test-one-module")
        class TestOneModule(module.Module):
            _package_requirements = [
                one_pkg_requirement,
            ]
            _gitrepo_requirements = []
            _command_requirements = []

        # install test-one-module
        mngr = eqp.ModuleEquipmentManager()
        mngr.sync(["test-one-module"])
        meta = mngr.meta["test-one-module"]

        # check that the package requirement is installed
        installation = get_installation(meta, one_pkg_requirement)
        assert installation is not None and installation.used_existing == True
        assert one_pkg_requirement.command in partial_ready_env.commands

        other_pkg_requirement = TestOtherPackageRequirement()

        # mick the update onto the package requirements
        # replace the package requirement from test-one-module
        TestOneModule._package_requirements.pop()
        TestOneModule._package_requirements.append(other_pkg_requirement)
        mngr.sync(["test-one-module"])

        # check that the one-package-requirement is replaced by other-package
        installation = get_installation(meta, one_pkg_requirement)
        assert installation is None
        installation = get_installation(meta, other_pkg_requirement)
        assert installation is not None and installation.used_existing == False
        # the command is not removed because it is not uninstalled by dofu
        assert one_pkg_requirement.command in partial_ready_env.commands
        assert other_pkg_requirement.command in partial_ready_env.commands
        assert meta.status == eqp.ModuleEquipmentStatus.INSTALLED

    @pytest.fixture(scope="function")
    def error_env(self):
        class ErrorExecEnv(ExecEnv):
            def install_package(self, package_manager, spec):
                # mock an error when install test-other-pkg
                if isinstance(package_manager, TestAvailPackageManager):
                    if spec == sp.PackageSpecification(package="test-other-pkg"):
                        raise RuntimeError("mock error")

            def uninstall_package(self, package_manager, spec):
                # mock an error when uninstall test-one-pkg
                if isinstance(package_manager, TestAvailPackageManager):
                    if spec == sp.PackageSpecification(package="test-one-pkg"):
                        raise RuntimeError("mock error")

        global mock_env
        mock_env = ErrorExecEnv()
        yield mock_env
        mock_env = None

    @classmethod
    def test_sync_with_error_env(cls, error_env: ExecEnv):
        """
        Test that the package requirement can be synchronized correctly
        when there are errors when install or uninstall the package.

        The error environment will raise an error when installing test-other-pkg,
        and raise an error when uninstalling test-one-pkg.
        """
        one_pkg_requirement = TestOnePackageRequirement()

        @module.Module.module("test-one-module")
        class TestOneModule(module.Module):
            _package_requirements = [
                one_pkg_requirement,
            ]
            _gitrepo_requirements = []
            _command_requirements = []

        # install test-one-module
        mngr = eqp.ModuleEquipmentManager()
        mngr.sync(["test-one-module"])
        meta = mngr.meta["test-one-module"]

        # check that the package requirement is installed
        installation = get_installation(meta, one_pkg_requirement)
        assert installation is not None and installation.used_existing == False
        assert one_pkg_requirement.command in error_env.commands
        assert meta.status == eqp.ModuleEquipmentStatus.INSTALLED

        # mick the update onto the package requirements
        # add one more package requirement to test-one-module
        other_pkg_requirement = TestOtherPackageRequirement()
        TestOneModule._package_requirements.append(other_pkg_requirement)

        # assert that the error is raised when installing test-other-pkg
        with pytest.raises(Exception, match="mock error"):
            mngr.sync(["test-one-module"])

        # check that the installed test-one-pkg is not influenced
        installation = get_installation(meta, one_pkg_requirement)
        assert installation is not None and installation.used_existing == False
        assert one_pkg_requirement.command in error_env.commands
        # check that the test-other-pkg failed to be installed
        assert other_pkg_requirement.command not in error_env.commands
        installation = get_installation(meta, other_pkg_requirement)
        assert installation is None
        assert meta.status == eqp.ModuleEquipmentStatus.BROKEN

        # mick the update onto the package requirements
        # remove the test-one-pkg from test-one-module
        TestOneModule._package_requirements.pop()
        TestOneModule._package_requirements.pop()

        # assert that the error is raised when installing test-other-pkg
        with pytest.raises(Exception, match="mock error"):
            mngr.sync(["test-one-module"])

        # check that the installed test-one-pkg is not uninstalled
        installation = get_installation(meta, one_pkg_requirement)
        assert installation is not None and installation.used_existing == False
        assert one_pkg_requirement.command in error_env.commands
        # check that the test-other-pkg is not installed
        installation = get_installation(meta, other_pkg_requirement)
        assert installation is None
        assert other_pkg_requirement.command not in error_env.commands


def get_installation(
    meta: eqp.ModuleEquipmentMetaInfo, requirement: req.PackageRequirement
):
    for installation in meta.package_installations:
        if installation.requirement == requirement:
            return installation
    return None

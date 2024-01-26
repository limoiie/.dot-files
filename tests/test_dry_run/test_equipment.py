import re

import pytest

from dofu import module, requirement as req
from dofu.equipment import ModuleEquipmentManager
from tests.dummies import DummyPackageRequirement, UCDummy
from tests.test_dry_run.conftest import under_temp_workspace


@module.Module.module("dummy", requires=[])
class DummyModule(module.Module):
    _package_requirements = [
        DummyPackageRequirement(),
    ]

    _gitrepo_requirements = [
        req.GitRepoRequirement(
            url="https://github.com/sarcasticadmin/empty-repo",
            path=under_temp_workspace("dummy-repo"),
        ),
    ]

    _command_requirements = [
        UCDummy(content="dummy-content"),
    ]


class TestDryRunEquipment:
    @pytest.fixture(autouse=True)
    def _enable_dry_run(self, enable_dry_run):
        pass

    def test_cli_sync(self, capsys):
        """
        Test that dry run does not execute the command.
        """

        # create temp manager for isolating the test
        manager = ModuleEquipmentManager()
        manager.sync(["dummy"])

        stdout = capsys.readouterr()

        messages = [
            # install package
            r'echo "pm-dummy install dummy-pkg"',
            # git clone repo
            r"git clone .*/empty-repo .*/dummy-repo",
            # execute config step
            r'echo "uc-dummy exec dummy-content"',
            # persist equipment
            r"move .*/equipment.yaml.dofu.tmp .*/equipment.yaml",
        ]

        # print("Captured stdout:")
        # print(stdout.out)

        pos = 0
        for message in messages:
            pattern = re.compile(message, re.MULTILINE)
            assert pattern.search(stdout.out, pos)
            pos = pattern.search(stdout.out, pos).end()


class TestNoDryRunEquipment:
    @pytest.fixture(autouse=True)
    def _disable_dry_run(self, disable_dry_run):
        pass

    def test_cli_sync(self, capfd):
        """
        Test that no dry dun does execute the command.
        """

        # create temp manager for isolating the test
        manager = ModuleEquipmentManager()
        manager.sync(["dummy"])

        stdout = capfd.readouterr()

        messages = [
            # dummy install package
            r"^pm-dummy install dummy-pkg",
            # dummy exec config step
            r"^uc-dummy exec dummy-content",
        ]

        # print("Captured stdout:")
        # print(stdout.out)

        pos = 0
        for message in messages:
            pattern = re.compile(message, re.MULTILINE)
            assert pattern.search(stdout.out, pos)
            pos = pattern.search(stdout.out, pos).end()

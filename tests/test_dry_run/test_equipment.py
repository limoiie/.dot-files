import logging
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

    def test_cli_sync(self, caplog):
        """
        Test that dry run does not execute the command.
        """

        # create temp manager for isolating the test
        manager = ModuleEquipmentManager()

        with caplog.at_level(logging.INFO):
            manager.sync(["dummy"])

        stdout = caplog.text

        messages = [
            # install package
            r'echo "pm-dummy install dummy-pkg"',
            # git clone repo
            r"git clone .*/empty-repo .*/dummy-repo",
            # execute config step
            r'echo "uc-dummy exec dummy-content"',
            # persist equipment
            r"mv .*/equipment.yaml.dofu.tmp .*/equipment.yaml",
        ]

        pos = 0
        for message in messages:
            pattern = re.compile(message, re.MULTILINE)
            assert pattern.search(stdout, pos)
            pos = pattern.search(stdout, pos).end()


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

        messages = [
            # dummy install package
            r"^pm-dummy install dummy-pkg",
            # dummy exec config step
            r"^uc-dummy exec dummy-content",
        ]

        out = capfd.readouterr().out

        pos = 0
        for message in messages:
            pattern = re.compile(message, re.MULTILINE)
            assert pattern.search(out, pos)
            pos = pattern.search(out, pos).end()

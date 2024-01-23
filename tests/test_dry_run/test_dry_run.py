import re

from dofu.equipment import ModuleEquipmentManager


class TestDryRun:
    def test_cli_sync(self, capsys, enable_dry_run):
        """
        Test that dry run does not execute the command.
        """

        manager = ModuleEquipmentManager.load()
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

        print("Captured stdout:")
        print(stdout.out)

        pos = 0
        for message in messages:
            pattern = re.compile(message, re.MULTILINE)
            assert pattern.search(stdout.out, pos)
            pos = pattern.search(stdout.out, pos).end()


class TestNoDryRun:
    def test_cli_sync(self, capfd, disable_dry_run):
        """
        Test that no dry dun does execute the command.
        """

        manager = ModuleEquipmentManager.load()
        manager.sync(["dummy"])

        stdout = capfd.readouterr()

        messages = [
            # dummy install package
            r"^pm-dummy install dummy-pkg",
            # dummy exec config step
            r"^uc-dummy exec dummy-content",
        ]

        print("Captured stdout:")
        print(stdout.out)

        pos = 0
        for message in messages:
            pattern = re.compile(message, re.MULTILINE)
            assert pattern.search(stdout.out, pos)
            pos = pattern.search(stdout.out, pos).end()

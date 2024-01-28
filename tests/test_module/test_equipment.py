import autoserde
import pytest

from dofu import equipment as eqp, module, requirement as req, undoable_commands as ucs
from tests.dummies import DummyPackageRequirement, UCDummy


class TestEquipmentSerde:
    @pytest.fixture(scope="function", autouse=True)
    def graph(self, registration_preserver):
        """
        This fixture is responsible to provide a clean graph for each test.

        Any registration happened during the test will be removed after the test.
        """
        yield registration_preserver

    def test_serde_package(self, tmp_path):
        package = DummyPackageRequirement()

        # serialize
        ser_file = tmp_path / "out.yaml"
        with open(ser_file, "w+") as out:
            autoserde.AutoSerde.serialize(package, out)

        # deserialize
        with open(ser_file, "r") as inp:
            package2 = autoserde.AutoSerde.deserialize(inp, cls=req.PackageRequirement)
        assert package == package2

    def test_serde_gitrepos(self, tmp_path):
        requirement = req.GitRepoRequirement(
            "https://github.com/some/repo.git",
            "some/path",
            submodule=True,
            branch="dev",
            commit_id="1234567890",
            depth=1,
        )

        # serialize
        ser_file = tmp_path / "out.yaml"
        with open(ser_file, "w+") as out:
            autoserde.AutoSerde.serialize(requirement, out)

        # deserialize
        with open(ser_file, "r") as inp:
            requirement2 = autoserde.AutoSerde.deserialize(
                inp, cls=req.GitRepoRequirement
            )
        assert requirement == requirement2

    def test_serde_commands(self, tmp_path):
        command = UCDummy("dummy-content")

        # serialize
        ser_file = tmp_path / "out.yaml"
        with open(ser_file, "w+") as out:
            autoserde.AutoSerde.serialize(command, out)

        # deserialize
        with open(ser_file, "r") as inp:
            command2 = autoserde.AutoSerde.deserialize(inp, cls=ucs.UCBackupMv)
        assert command == command2

    def test_serde_equipment(self, tmp_path):
        # noinspection PyUnusedLocal
        @module.Module.module("dummy", requires=[])
        class DummyModule(module.Module):
            _package_requirements = [
                DummyPackageRequirement(),
            ]

            _gitrepo_requirements = [
                req.GitRepoRequirement(
                    url="https://github.com/sarcasticadmin/empty-repo",
                    path=str(tmp_path / "dummy-repo"),
                ),
            ]

            _command_requirements = [
                UCDummy(content="dummy-content"),
            ]

        # sync and serialize
        mngr = eqp.ModuleEquipmentManager()
        mngr.sync(["dummy"])

        # deserialize
        loaded_mngr = eqp.ModuleEquipmentManager.load()
        assert mngr == loaded_mngr

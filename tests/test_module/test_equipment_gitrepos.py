import re
import shutil

import pytest

from dofu import (
    env,
    equipment as eqp,
    module,
    requirement as req,
    version_control as vc,
)


class TestEquipmentSyncGitRepos:
    @pytest.fixture(scope="function", autouse=True)
    def graph(self, registration_preserver):
        """
        This fixture is responsible to provide a clean graph for each test.

        Any registration happened during the test will be removed after the test.
        """
        yield registration_preserver

    @pytest.fixture(scope="function")
    def prepare_module(self, tmp_path):
        """
        Prepare a module with a git repo requirement for testing sync.
        """
        dst_repo_path = tmp_path / "dummy-repo"
        requirement = req.GitRepoRequirement(
            url="https://github.com/sarcasticadmin/empty-repo.git",
            path=dst_repo_path,
        )

        # noinspection PyUnusedLocal
        @module.Module.module("test-one-module")
        class TestOneModule(module.Module):
            _package_requirements = []
            _gitrepo_requirements = [
                requirement,
            ]
            _command_requirements = []

        yield dst_repo_path, requirement, TestOneModule

    def test_sync_moving_repo(self, capfd, tmp_path, prepare_module):
        dst_repo_path, requirement, TestOneModule = prepare_module
        new_repo_path = tmp_path / "dummy-repo-moved"

        # install test-one-module
        mngr = eqp.ModuleEquipmentManager()
        mngr.sync(["test-one-module"])
        meta = mngr.meta["test-one-module"]

        # assert the git clone occurs
        assert "Cloning into" in capfd.readouterr().err

        # assert the installation is correct
        installation = get_installation(meta, requirement)
        assert installation is not None
        assert installation.requirement.url == requirement.url
        assert dst_repo_path.samefile(installation.requirement.path)
        assert installation.used_existing == False

        # mick the requirements change
        # move the repo
        new_requirement = req.GitRepoRequirement(
            url=requirement.url,
            path=new_repo_path,
        )
        TestOneModule._gitrepo_requirements = [
            new_requirement,
        ]

        # assert no clone occurs
        assert capfd.readouterr().out == ""
        assert capfd.readouterr().err == ""

        # sync test-one-module again
        mngr.sync(["test-one-module"])

        # assert update the moved repo
        assert re.match(r".*up to date.*", capfd.readouterr().out)

        # assert the local repo has been moved
        assert new_repo_path.exists()
        assert not dst_repo_path.exists()

        # assert the installation is correct
        installation = get_installation(meta, new_requirement)
        assert installation is not None
        assert installation.requirement.url == new_requirement.url
        assert new_repo_path.samefile(installation.requirement.path)
        assert installation.used_existing == False

    def test_sync_existing_same_repo(self, capfd, tmp_path, prepare_module):
        dst_repo_path, requirement, _ = prepare_module

        # create the repo
        vc.clone(repo=requirement.url, repo_path=dst_repo_path)

        # install test-one-module
        mngr = eqp.ModuleEquipmentManager()
        mngr.sync(["test-one-module"])
        meta = mngr.meta["test-one-module"]

        # assert no git clone occurs
        assert capfd.readouterr().out == ""

        # assert the installation is correct
        installation = get_installation(meta, requirement)
        assert installation is not None
        assert installation.requirement.url == requirement.url
        assert dst_repo_path.samefile(installation.requirement.path)
        assert installation.used_existing == True

    def test_sync_existing_other_repo(self, capfd, tmp_path, prepare_module):
        dst_repo_path, requirement, _ = prepare_module

        # another repo
        shutil.copytree(env.project_root(), dst_repo_path)

        # install test-one-module
        mngr = eqp.ModuleEquipmentManager()
        with pytest.raises(RuntimeError, match="git clone.*already exists"):
            mngr.sync(["test-one-module"])
        meta = mngr.meta["test-one-module"]

        # assert the installation is correct
        installation = get_installation(meta, requirement)
        assert installation is None


def get_installation(
    meta: eqp.ModuleEquipmentMetaInfo, requirement: req.GitRepoRequirement
):
    for installation in meta.gitrepo_installations:
        if installation.requirement.url == requirement.url:
            return installation
    return None

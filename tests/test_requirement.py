import shutil
import subprocess

import pytest

from dofu import requirement as req, version_control as vc, env


@pytest.fixture(scope="function")
def repo_url_path(tmp_path):
    url = "https://github.com/sarcasticadmin/empty-repo"
    path = tmp_path / "dummy-repo"
    return url, path


class TestGitRepoRequirement:
    def test_normal(self, capfd, repo_url_path):
        repo_url, path = repo_url_path
        requirement = req.GitRepoRequirement(url=repo_url, path=path)

        assert not requirement.is_satisfied()

        # install
        requirement.install()
        assert capfd.readouterr().err.startswith("Cloning into")
        assert requirement.is_satisfied()
        assert path.exists()
        assert vc.current_commit_id(repo_path=path).startswith("7fee966")

        # uninstall
        requirement.uninstall()
        assert not requirement.is_satisfied()
        assert not path.exists()

    def test_with_commit_id(self, capfd, repo_url_path):
        repo_url, path = repo_url_path
        requirement = req.GitRepoRequirement(
            url=repo_url, path=path, commit_id="79005a0"
        )

        # install
        requirement.install()
        assert capfd.readouterr().err.startswith("Cloning into")
        assert path.exists()
        assert vc.current_commit_id(repo_path=path).startswith("79005a0")

    def test_with_branch(self, capfd, repo_url_path):
        repo_url, path = repo_url_path
        requirement = req.GitRepoRequirement(
            url=repo_url, path=path, branch="rh/1650041898"
        )

        # install
        requirement.install()
        assert capfd.readouterr().err.startswith("Cloning into")
        assert path.exists()
        assert vc.current_commit_id(repo_path=path).startswith("774845a")

    def test_error_with_existing_repo(self, capfd, repo_url_path):
        repo_url, path = repo_url_path
        requirement = req.GitRepoRequirement(url=repo_url, path=path)

        # create a dummy repo at the path
        shutil.copytree(env.project_root(), path)

        assert not requirement.is_satisfied()

        # install
        with pytest.raises(subprocess.CalledProcessError):
            requirement.install()

        assert capfd.readouterr().err.startswith("fatal: destination path")

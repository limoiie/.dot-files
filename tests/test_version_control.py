import pytest


@pytest.fixture(scope="class")
def demo_repo_url():
    return "https://github.com/sarcasticadmin/empty-repo.git"


class TestVersionControl:
    def test_clone(self, capfd, tmp_path, demo_repo_url):
        from dofu.version_control import clone

        assert not (tmp_path / "empty-repo").exists()
        assert not (tmp_path / "specified-empty-repo").exists()

        # clone to default path
        clone(repo=demo_repo_url, cwd=tmp_path)
        assert (tmp_path / "empty-repo").exists()
        assert not (tmp_path / "specified-empty-repo").exists()

        assert "Cloning into" in capfd.readouterr().err

        # clone to specified path
        clone(repo=demo_repo_url, repo_path=tmp_path / "specified-empty-repo")
        assert (tmp_path / "empty-repo").exists()
        assert (tmp_path / "specified-empty-repo").exists()

        assert "Cloning into" in capfd.readouterr().err

    def test_last_commit_id_and_default_branch(self, capfd, tmp_path, demo_repo_url):
        from dofu.version_control import clone, last_commit_id_of, default_branch

        # clone to default path
        clone(repo=demo_repo_url, cwd=tmp_path)

        assert (
            last_commit_id_of(repo_path=tmp_path / "empty-repo")
            == "7fee966df87831bc18851d727a35acec8a29e0b5"
        )
        assert (
            last_commit_id_of(repo_path=tmp_path / "empty-repo", path=".gitignore")
            == "7fee966df87831bc18851d727a35acec8a29e0b5"
        )
        assert (
            last_commit_id_of(repo_path=tmp_path / "empty-repo", path="README.md")
            == "79005a0b56bd233dafa4fa75be79dc03a067a349"
        )

        capfd.readouterr()

        assert default_branch(repo_path=tmp_path / "empty-repo") == "master"

    def test_checkout(self, capfd, tmp_path, demo_repo_url):
        from dofu.version_control import clone, checkout, last_commit_id_of

        # clone to default path
        clone(repo=demo_repo_url, cwd=tmp_path)
        assert "Cloning into" in capfd.readouterr().err
        assert (
            last_commit_id_of(repo_path=tmp_path / "empty-repo")
            == "7fee966df87831bc18851d727a35acec8a29e0b5"
        )

        # checkout to HEAD~1
        checkout(repo_path=tmp_path / "empty-repo", revision="HEAD~1")
        assert "switching to 'HEAD~1'" in capfd.readouterr().err
        assert (
            last_commit_id_of(repo_path=tmp_path / "empty-repo")
            == "79005a0b56bd233dafa4fa75be79dc03a067a349"
        )

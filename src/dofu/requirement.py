import abc
import dataclasses
import os.path
import subprocess
import typing as t

from dofu import (
    package_manager as pm,
    platform as pf,
    shutils,
    utils,
    version_control as vc,
)


class Requirement(abc.ABC):
    @abc.abstractmethod
    def install(self):
        pass

    @abc.abstractmethod
    def uninstall(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def update(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def is_satisfied(self):
        """
        Check if the requirement is satisfied.
        The requirement can be satisfied even if the requirement is not installed.

        :return: True if the requirement is satisfied, False otherwise.
        """
        pass


@dataclasses.dataclass
class GitRepoRequirement(Requirement):
    """
    A requirement of a git repository.
    """

    repo: str
    """
    The URL of the git repository.
    """

    path: str
    """
    The path to the git repository.
    """

    submodule: t.Optional[bool] = None
    """
    Whether to clone the submodules.
    """

    branch: t.Optional[str] = None
    """
    The branch to checkout.
    """

    commit_id: t.Optional[str] = None
    """
    The commit id to checkout.
    """

    depth: t.Optional[int] = None
    """
    The depth of the git repository.
    """

    def install(self):
        vc.clone(
            *[f"--branch={branch}" for branch in opt(self.branch)],
            *[f"--depth={depth}" for depth in opt(self.depth)],
            *[f"--submodules={submodules}" for submodules in opt(self.submodule)],
            repo=self.repo,
            repo_path=self.path,
        )
        if self.commit_id is not None:
            vc.checkout(repo_path=self.path, revision=self.commit_id)

    def uninstall(self):
        if os.path.isdir(self.path):
            shutils.rmtree(self.path)
            return True
        return False

    def update(self):
        branch = self.branch or vc.default_branch(self.path)
        vc.fetch("origin", branch, repo_path=self.path)
        vc.checkout(repo_path=self.path, revision=branch)
        if self.commit_id is not None:
            vc.checkout(repo_path=self.path, revision=self.commit_id)

    def is_satisfied(self):
        with utils.supress(subprocess.CalledProcessError):
            return os.path.isdir(self.path) and (
                vc.remote_get_url(repo_path=self.path, name="origin") == self.repo_url
            )
        # noinspection PyUnreachableCode
        return False

    @property
    def repo_url(self):
        url = self.repo.rstrip("/")
        if not url.endswith(".git"):
            url += ".git"
        return url


@dataclasses.dataclass
class PackageRequirement(Requirement):
    """
    A requirement of a package.
    """

    _pkg_manager_candidates: t.ClassVar[t.Dict[pf.Platform, pm.PackageManager]]
    """
    A dictionary indicating which package managers should be used on what platform.
    
    NOTE: this field will be ignored by dataclass init
    """

    package: str
    version: str
    command: str

    def install(self):
        """
        Install the tool using the first available package manager.

        :return: The package manager used to install the tool.
        """
        for platform, pkg_manager in self._pkg_manager_candidates.items():
            if platform():
                if pkg_manager.install(self.package):
                    return pkg_manager
        return None

    def update(self, pkg_manager: pm.PackageManager):
        """
        Update the tool using the given package manager.

        :param pkg_manager:
        :return: The package manager used to update the tool.
        """
        if pkg_manager.update(self.package):
            return pkg_manager
        return None

    def uninstall(self, pkg_manager: pm.PackageManager):
        """
        Uninstall the tool using the given package manager.

        :param pkg_manager: The package manager to use to uninstall the tool.
        :return: The package manager used to uninstall the tool.
        """
        if pkg_manager.uninstall(self.package):
            return pkg_manager
        return None

    def is_satisfied(self):
        return shutils.do_commands_exist(self.command)


@dataclasses.dataclass
class PackageInstallationMetaInfo:
    """
    Meta information about the installation of a package.
    """

    requirement: PackageRequirement
    """
    The requirement of the package that is installed.
    """

    manager: t.Optional[pm.PackageManager]
    """
    The manager has been used to install the package.
    """

    used_existing: bool
    """
    Whether the package has been installed before.
    """


@dataclasses.dataclass
class GitRepoInstallationMetaInfo:
    """
    Meta information about the installation of a git repository.
    """

    requirement: GitRepoRequirement
    """
    The requirement of the git repository that is installed.
    """

    used_existing: bool
    """
    Whether the repo has been cloned before.
    """


def opt(obj, *, empty=None):
    if obj is not empty:
        yield obj

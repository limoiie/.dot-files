import abc
import dataclasses
import os.path
import typing as t

import dofu.version_control as vc
from dofu import package_manager as pm, platform as pf, shutils


class Requirement(abc.ABC):
    @abc.abstractmethod
    def install(self):
        pass

    @abc.abstractmethod
    def uninstall(self):
        pass

    @abc.abstractmethod
    def update(self):
        pass

    @abc.abstractmethod
    def is_installed(self):
        """
        Check if the tool is installed.

        :return: True if the tool is installed, False otherwise.
        """
        pass


@dataclasses.dataclass
class GitRepoRequirement:
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
        opts = [
            *[f"--branch={branch}" for branch in opt(self.branch)],
            *[f"--depth={depth}" for depth in opt(self.depth)],
            *[f"--submodules={submodules}" for submodules in opt(self.submodule)],
        ]
        vc.clone(*opts, repo=self.repo, repo_path=self.path)
        if self.commit_id is not None:
            vc.checkout(repo_path=self.path, revision=self.commit_id)

    def uninstall(self):
        shutils.rmtree(self.path)

    def update(self):
        branch = self.branch or vc.default_branch(self.path)
        vc.fetch("origin", branch, repo_path=self.path)
        vc.checkout(repo_path=self.path, revision=branch)
        if self.commit_id is not None:
            vc.checkout(repo_path=self.path, revision=self.commit_id)

    def is_installed(self):
        return os.path.isdir(self.path)


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

    def update(self):
        # TODO: need implementation
        raise NotImplementedError

    def uninstall(self, pkg_manager: pm.PackageManager = None):
        """
        Uninstall the tool using the given package manager if provided.
        Otherwise, the first available package manager is used.

        :param pkg_manager: The package manager to use to uninstall the tool.
        :return: The package manager used to uninstall the tool.
        """
        if pkg_manager:
            if pkg_manager.uninstall(self.package):
                return pkg_manager
            return None

        for platform, pkg_manager in self._pkg_manager_candidates.items():
            if platform():
                if pkg_manager.uninstall(self.package):
                    return pkg_manager
        return None

    def is_installed(self):
        return shutils.do_commands_exist(self.command)


@dataclasses.dataclass
class PRRustup(PackageRequirement):
    _pkg_manager_candidates = {
        pf.LINUX: pm.CurlShPackageManager(
            "curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh",
            "rustup self uninstall",
        ),
    }

    package: str = "rustup"
    version: str = "latest"
    command: str = "rustup"


@dataclasses.dataclass
class PRBob(PackageRequirement):
    _pkg_manager_candidates = {
        pf.ANY: pm.CargoPackageManager(),
    }

    package: str = "bob-nvim"
    version: str = "latest"
    command: str = "bob"


@dataclasses.dataclass
class PRNeovim(PackageRequirement):
    _pkg_manager_candidates = {
        pf.ANY: pm.BobNvimPackageManager(),
    }

    package: str = "neovim"
    version: str = "latest"
    command: str = "nvim"


@dataclasses.dataclass
class PackageInstallationMetaInfo:
    """
    Meta information about the installation of a package.
    """

    requirement: PackageRequirement
    """
    The requirement of the package that is installed.
    """

    manager: pm.PackageManager
    """
    The manager has been used to install the package.
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


def opt(obj, *, empty=None):
    if obj is not empty:
        yield obj

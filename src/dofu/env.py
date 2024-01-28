import functools
import os.path
import pathlib


def dot_config_path(*nested: os.PathLike) -> os.PathLike:
    return os.path.join(project_root(), "xdg-config", *nested)


def xdg_config_path(*nested: os.PathLike) -> os.PathLike:
    return os.path.join(user_home(), ".config", *nested)


def user_home_path(*nested: os.PathLike) -> os.PathLike:
    return os.path.join(user_home(), *nested)


def project_path(*nested: os.PathLike) -> os.PathLike:
    return os.path.join(project_root(), *nested)


def dot_config_path_relhome(*nested: os.PathLike) -> os.PathLike:
    relpath = os.path.relpath(dot_config_path(*nested), user_home())
    return os.path.join("$HOME", relpath)


def xdg_config_path_relhome(*nested: os.PathLike) -> os.PathLike:
    relpath = os.path.relpath(xdg_config_path(*nested), user_home())
    return os.path.join("$HOME", relpath)


def project_path_relhome(*nested: os.PathLike) -> os.PathLike:
    relpath = os.path.relpath(project_path(*nested), user_home())
    return os.path.join("$HOME", relpath)


@functools.cache
def user_home() -> os.PathLike:
    return os.path.expanduser("~")


@functools.cache
def project_root() -> os.PathLike:
    """
    The root of this project.

    It is found by looking for pyproject.toml
    """
    folder = pathlib.Path(__file__).parent
    while not os.path.exists(folder / "pyproject.toml"):
        folder = folder.parent
    return folder


def cache_root() -> os.PathLike:
    root = os.path.join(project_root(), ".cache")
    if not os.path.exists(root):
        os.makedirs(root)
    return root


def persistence_root() -> os.PathLike:
    root = os.path.join(cache_root(), ".persistence")
    if not os.path.exists(root):
        os.makedirs(root)
    return root


def equipment_persistence_file() -> os.PathLike:
    return os.path.join(persistence_root(), "equipment.yaml")

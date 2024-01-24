from dofu.module import ModuleRegistrationManager

from .neovim import NeovimModule
from .rust import RustModule

__all__ = [
    "NeovimModule",
    "RustModule",
]


ModuleRegistrationManager.validate()

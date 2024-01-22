from ..module import ModuleRegistrationManager

from .neovim import NeovimModule
from .rust import RustModule


ModuleRegistrationManager.validate()

from dofu.module import ModuleRegistrationManager

from .cargo_crates import CargoCratesModule
from .emacs import EmacsModule
from .fzf import FzfModule
from .go_mods import GoModsModule
from .golang import GolangModule
from .neovim import NeovimModule
from .rust import RustModule
from .starship import StarshipModule
from .tmux import TmuxModule
from .vim import VimModule
from .zsh import ZshModule

__all__ = [
    "CargoCratesModule",
    "EmacsModule",
    "FzfModule",
    "GoModsModule",
    "GolangModule",
    "NeovimModule",
    "RustModule",
    "StarshipModule",
    "TmuxModule",
    "VimModule",
    "ZshModule",
]


ModuleRegistrationManager.validate()

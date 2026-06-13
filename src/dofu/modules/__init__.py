from dofu.module import ModuleRegistrationManager

from .emacs import EmacsModule
from .neovim import NeovimModule
from .tmux import TmuxModule
from .zsh import ZshModule

__all__ = [
    "EmacsModule",
    "NeovimModule",
    "TmuxModule",
    "ZshModule",
]


ModuleRegistrationManager.validate()

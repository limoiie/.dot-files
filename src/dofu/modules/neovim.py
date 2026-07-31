from dofu import (
    env,
    undoable_commands as ucs,
)
from dofu.module import Module


@Module.module("neovim", requires=[])
class NeovimModule(Module):
    # neovim itself is now managed by mise (see xdg-config/mise/config.toml).
    # This module only owns the NvChad config symlink, which is a dotfile-style
    # change better suited to dofu than to mise. NvChad itself and all of its
    # plugins are installed by lazy.nvim at first nvim launch
    # (see xdg-config/NvChad/init.lua), so nothing needs to be cloned here.
    _package_requirements = []

    _gitrepo_requirements = []

    _command_requirements = [
        # link the whole custom NvChad config directory
        ucs.UCSymlink(
            src=env.dot_config_path("NvChad"),
            dst=env.xdg_config_path("NvChad"),
        ),
    ]

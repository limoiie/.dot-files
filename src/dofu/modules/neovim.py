from dofu import (
    env,
    requirement as req,
    undoable_commands as ucs,
)
from dofu.module import Module


@Module.module("neovim", requires=[])
class NeovimModule(Module):
    # neovim itself is now managed by mise (see xdg-config/mise/config.toml).
    # This module only owns the neovim config frameworks and the custom
    # NvChad config symlink, which are dotfile-style changes better suited
    # to dofu than to mise.
    _package_requirements = []

    _gitrepo_requirements = [
        # download three neovim config frameworks
        req.GitRepoRequirement(
            url="https://github.com/NvChad/NvChad.git",
            path=env.xdg_config_path("NvChad"),
        ),
        req.GitRepoRequirement(
            url="https://github.com/AstroNvim/AstroNvim.git",
            path=env.xdg_config_path("AstroNvim"),
        ),
        req.GitRepoRequirement(
            url="https://github.com/LazyVim/starter.git",
            path=env.xdg_config_path("LazyVim"),
        ),
    ]

    _command_requirements = [
        # apply custom NvChad config
        ucs.UCSymlink(
            src=env.dot_config_path("NvChad", "lua", "custom"),
            dst=env.xdg_config_path("NvChad", "lua", "custom"),
        ),
    ]

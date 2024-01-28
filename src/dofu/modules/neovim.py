from dofu import (
    env,
    package_requirements as prs,
    requirement as req,
    undoable_commands as ucs,
)
from dofu.module import Module
from .rust import RustModule


@Module.module("neovim", requires=[RustModule])
class NeovimModule(Module):
    _package_requirements = [
        prs.PRCargoCrate.make(name="bob-nvim", command="bob"),
        prs.PRNeovim(),
    ]

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
        # add bob/nvim-bin to PATH to use the latest neovim
        ucs.UCAppendEnvVarPath(
            "$HOME/.local/share/bob/nvim-bin", env.user_home_path(".bashrc")
        ),
        ucs.UCAppendEnvVarPath(
            "$HOME/.local/share/bob/nvim-bin", env.user_home_path(".zshrc")
        ),
        # apply custom NvChad config
        ucs.UCSymlink(
            src=env.dot_config_path("NvChad", "lua", "custom"),
            dst=env.xdg_config_path("NvChad", "lua", "custom"),
        ),
    ]

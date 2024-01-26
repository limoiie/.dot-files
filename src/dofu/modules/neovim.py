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
        prs.PRBob(),
        prs.PRNeovim(),
    ]

    _gitrepo_requirements = [
        req.GitRepoRequirement(
            url="https://github.com/NvChad/NvChad.git",
            path=env.xdg_config_path("NvChad"),
        ),
    ]

    _command_requirements = [
        ucs.UCBackupMv(path=env.xdg_config_path("NvChad")),
        ucs.UCSymlink(
            src=env.dot_config_path("NvChad", "lua", "custom"),
            dst=env.xdg_config_path("NvChad", "lua", "custom"),
        ),
    ]

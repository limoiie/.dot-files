from dofu import env, requirements as req, undoable_command as uc
from dofu.module import Module
from .rust import RustModule


@Module.module("neovim", requires=[RustModule])
class NeovimModule(Module):
    _package_requirements = [
        req.PRBob(),
        req.PRNeovim(),
    ]

    _git_repo_requirements = [
        req.GitRepoRequirement(
            repo="https://github.com/NvChad/NvChad.git",
            path=env.xdg_config_path("NvChad"),
        ),
    ]

    _config_steps = [
        uc.UCBackupMv(path=env.xdg_config_path("NvChad")),
        uc.UCLink(
            src=env.dot_config_path("NvChad", "lua", "custom"),
            dst=env.xdg_config_path("NvChad", "lua", "custom"),
        ),
    ]

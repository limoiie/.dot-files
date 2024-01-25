import dofu.package_requirements.bob_nvim
import dofu.package_requirements.neovim
from dofu import env, requirement as req, undoable_command as uc
from dofu.module import Module
from .rust import RustModule


@Module.module("neovim", requires=[RustModule])
class NeovimModule(Module):
    _package_requirements = [
        dofu.package_requirements.bob_nvim.PRBob(),
        dofu.package_requirements.neovim.PRNeovim(),
    ]

    _gitrepo_requirements = [
        req.GitRepoRequirement(
            url="https://github.com/NvChad/NvChad.git",
            path=env.xdg_config_path("NvChad"),
        ),
    ]

    _command_requirements = [
        uc.UCBackupMv(path=env.xdg_config_path("NvChad")),
        uc.UCSymlink(
            src=env.dot_config_path("NvChad", "lua", "custom"),
            dst=env.xdg_config_path("NvChad", "lua", "custom"),
        ),
    ]

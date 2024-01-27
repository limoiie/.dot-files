from dofu import env, undoable_commands as ucs
from dofu.module import Module
from dofu.modules.rust import RustModule


@Module.module("vim", requires=[RustModule])
class VimModule(Module):
    _package_requirements = []

    _gitrepo_requirements = []

    _command_requirements = [
        # prepare vim config directory
        ucs.UCMkdir(path=env.xdg_config_path("vim")),
        # move dotfiles to XDG_CONFIG_HOME
        ucs.UCSafeMove(
            src=env.user_home_path(".vimrc"),
            dst=env.xdg_config_path("vim", "vimrc"),
        ),
        ucs.UCSafeMove(
            src=env.user_home_path(".viminfo"),
            dst=env.xdg_config_path("vim", "viminfo"),
        ),
        # append 'source the dotfiles' to vimrc
        ucs.UCAppendLine(
            path=env.xdg_config_path("vim", "vimrc"),
            pattern=".*common-vimrc",
            repl=f"source {env.project_path('common-vimrc')}",
        ),
    ]

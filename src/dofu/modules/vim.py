from dofu import env, package_requirements as prs, undoable_commands as ucs
from dofu.module import Module
from dofu.modules.rust import RustModule


@Module.module("vim", requires=[RustModule])
class VimModule(Module):
    _package_requirements = [
        prs.PRSystem.make("vim"),
    ]

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
        # setup ideavimrc
        ucs.UCLink(
            src=env.project_path(".ideavimrc"),
            dst=env.user_home_path(".ideavimrc"),
        ),
        # append 'source the dotfiles' to vimrc
        ucs.UCAppendLine(
            path=env.xdg_config_path("vim", "vimrc"),
            pattern=".*common-vimrc",
            repl=f"source {env.project_path('common-vimrc')}",
        ),
    ]

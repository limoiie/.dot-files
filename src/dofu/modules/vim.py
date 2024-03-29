from dofu import env, package_requirements as prs, undoable_commands as ucs
from dofu.module import Module


@Module.module("vim", requires=[])
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
        ucs.UCSymlink(
            src=env.project_path(".ideavimrc"),
            dst=env.user_home_path(".ideavimrc"),
        ),
        # append 'source the dotfiles' to vimrc
        ucs.UCAppendLine.make_source_line(
            path=env.xdg_config_path("vim", "vimrc"),
            pattern=".*common-vimrc",
            file_to_source=env.project_path_relhome("common-vimrc"),
            check_exists=False,
        ),
    ]

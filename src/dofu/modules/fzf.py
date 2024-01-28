from dofu import env, undoable_commands as ucs, package_requirements as prs
from dofu.module import Module


@Module.module("fzf", requires=[])
class FzfModule(Module):
    _package_requirements = [
        prs.PRSystem.make(name="fzf"),
    ]

    _gitrepo_requirements = []

    _command_requirements = [
        # move dotfiles to XDG_CONFIG_HOME
        ucs.UCSafeMove.make_home_to_xdg_config(src=".fzf.bash", dst="fzf.bash"),
        ucs.UCSafeMove.make_home_to_xdg_config(src=".fzf.zsh", dst="fzf.zsh"),
        # append 'source the dotfiles' to shell rc files
        ucs.UCAppendLine.make_source_line(
            path=env.user_home_path(".bashrc"),
            pattern=r"\-f.*fzf.bash",
            file_to_source=env.xdg_config_path_relhome("fzf.bash"),
        ),
        ucs.UCAppendLine.make_source_line(
            path=env.user_home_path(".zshrc"),
            pattern=r"\-f.*fzf.zsh",
            file_to_source=env.xdg_config_path_relhome("fzf.zsh"),
        ),
    ]

from dofu import (
    env,
    package_requirements as prs,
    requirement as req,
    undoable_commands as ucs,
)
from dofu.module import Module


@Module.module("zsh", requires=[])
class ZshModule(Module):
    _package_requirements = [
        prs.PRSystem.make(name="zsh"),
    ]

    _gitrepo_requirements = [
        req.GitRepoRequirement(
            url="https://github.com/zplug/zplug.git",
            path=env.xdg_config_path("zplug"),
        ),
    ]

    _command_requirements = [
        # use zsh as the default shell
        ucs.UCChSh(shell="zsh"),
        # prefer zplug in XDG_CONFIG_HOME instead of ~/.zplug
        ucs.UCBackupMv(path=env.user_home_path(".zplug")),
        # append "source the rc files" to shell rc files
        ucs.UCAppendLine.make_source_line(
            path=env.user_home_path(".zshrc"),
            pattern=".*common-shrc",
            file_to_source=env.project_path("common-shrc"),
        ),
        ucs.UCAppendLine.make_source_line(
            path=env.user_home_path(".zshrc"),
            pattern=".*common-zshrc",
            file_to_source=env.project_path("common-zshrc"),
        ),
    ]

from dofu import env, package_requirements as prs, undoable_commands as ucs
from dofu.module import Module


@Module.module("golang", requires=[])
class GolangModule(Module):
    _package_requirements = [
        prs.PRGolang(),
    ]

    _gitrepo_requirements = []

    _command_requirements = [
        ucs.UCAppendEnvVarPath(
            "/usr/local/go/bin:$HOME/go/bin", env.user_home_path(".bashrc")
        ),
        ucs.UCAppendEnvVarPath(
            "/usr/local/go/bin:$HOME/go/bin", env.user_home_path(".zshrc")
        ),
    ]

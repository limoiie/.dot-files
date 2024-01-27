from dofu import env, package_requirements as prs, undoable_commands as ucs
from dofu.module import Module


@Module.module("rust", requires=[])
class RustModule(Module):
    _package_requirements = [
        prs.PRRustup(),
    ]

    _gitrepo_requirements = []

    _command_requirements = [
        ucs.UCAppendEnvVarPath("$HOME/.cargo/bin", env.user_home_path(".bashrc")),
        ucs.UCAppendEnvVarPath("$HOME/.cargo/bin", env.user_home_path(".zshrc")),
    ]

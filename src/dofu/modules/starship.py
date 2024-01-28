from dofu import env, package_requirements as prs, undoable_commands as ucs
from dofu.module import Module


@Module.module("starship", requires=[])
class StarshipModule(Module):
    _package_requirements = [
        prs.PRStarship(),
    ]

    _gitrepo_requirements = []

    _command_requirements = [
        *ucs.UCAppendEnvVar.make_multiple_rcs(
            "USE_STARSHIP_THEME",
            "",
            env.user_home_path(".zshrc"),
            env.user_home_path(".bashrc"),
        ),
        *ucs.UCAppendEnvVar.make_multiple_rcs(
            "STARSHIP_CONFIG",
            env.dot_config_path_relhome("starship.toml"),
            env.user_home_path(".zshrc"),
            env.user_home_path(".bashrc"),
        ),
    ]

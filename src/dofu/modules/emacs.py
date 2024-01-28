from dofu import env, package_requirements as prs, requirement as req
from dofu.module import Module


@Module.module("emacs", requires=[])
class EmacsModule(Module):
    _package_requirements = [
        prs.PRSystem.make("emacs"),
    ]

    _gitrepo_requirements = [
        req.GitRepoRequirement(
            url="https://github.com/syl20bnr/spacemacs.git",
            path=env.user_home_path(".emacs.d"),
        ),
        req.GitRepoRequirement(
            url="https://github.com/limoiie/limo-spacemacs-layers.git",
            path=env.user_home_path(".emacs.d/private/layers"),
        ),
        # req.GitRepoRequirement(
        #     url="https://github.com/d12frosted/elpa-mirror.git",
        #     path=env.user_home_path(".emacs.d/private/elpa-mirror"),
        #     depth=1,
        # )
    ]

    _command_requirements = []

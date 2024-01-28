from dofu import (
    env,
    package_requirements as prs,
    requirement as req,
    undoable_commands as ucs,
)
from dofu.module import Module


@Module.module("tmux", requires=[])
class TmuxModule(Module):
    _package_requirements = [
        prs.PRSystem.make("tmux"),
    ]

    _gitrepo_requirements = [
        # download the oh-my-tmux framework
        req.GitRepoRequirement(
            url="https://github.com/gpakosz/.tmux.git",
            path=env.xdg_config_path("oh-my-tmux"),
        ),
    ]

    _command_requirements = [
        # prepare tmux config directory
        ucs.UCMkdir(path=env.xdg_config_path("tmux")),
        # use the oh-my-tmux framework
        ucs.UCSymlink(
            src=env.xdg_config_path("oh-my-tmux", ".tmux.conf"),
            dst=env.xdg_config_path("tmux", "tmux.conf"),
        ),
        # use the custom config
        ucs.UCSymlink(
            src=env.dot_config_path("tmux", "tmux.conf.local"),
            dst=env.xdg_config_path("tmux", "tmux.conf.local"),
        ),
    ]

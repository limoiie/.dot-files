from dofu import package_requirements as prs
from dofu.module import Module
from dofu.modules.golang import GolangModule


@Module.module("go-mods", requires=[GolangModule])
class GoModsModule(Module):
    _package_requirements = [
        prs.PRGoMod.make("github.com/jesseduffield/lazydocker", command="lazydocker"),
        prs.PRGoMod.make("github.com/jesseduffield/lazygit", command="lazygit"),
    ]

    _gitrepo_requirements = []

    _command_requirements = []

from dofu import package_requirements as prs
from dofu.module import Module


@Module.module("Starship", requires=[])
class StarshipModule(Module):
    _package_requirements = [
        prs.PRStarship(),
    ]

    _gitrepo_requirements = []

    _command_requirements = []

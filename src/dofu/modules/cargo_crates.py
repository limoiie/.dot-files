from dofu import package_requirements as prs
from dofu.module import Module
from dofu.modules.rust import RustModule


@Module.module("cargo-crates", requires=[RustModule])
class CargoCratesModule(Module):
    _package_requirements = [
        prs.PRCargoCrate.make(name="bat"),
        prs.PRCargoCrate.make(name="exa"),
        prs.PRCargoCrate.make(name="fd-find", command="fd"),
        prs.PRCargoCrate.make(name="procs"),
        prs.PRCargoCrate.make(name="ripgrep", command="rg"),
        prs.PRCargoCrate.make(name="sd"),
    ]

    _gitrepo_requirements = []

    _command_requirements = []

from dofu.module import Module
from dofu.requirements import PRRustup


@Module.module("rust", requires=[])
class RustModule(Module):
    _package_requirements = [
        PRRustup(),
    ]

    _gitrepo_requirements = []

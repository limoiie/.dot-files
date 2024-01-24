import abc
import dataclasses

from dofu import specification as sp


@dataclasses.dataclass
class PackageManager(abc.ABC):
    @abc.abstractmethod
    def install(self, spec: sp.PackageSpecification) -> bool:
        pass

    @abc.abstractmethod
    def uninstall(self, spec: sp.PackageSpecification) -> bool:
        pass

    @abc.abstractmethod
    def update(self, spec: sp.PackageSpecification) -> bool:
        pass

    @abc.abstractmethod
    def is_available(self) -> bool:
        return False

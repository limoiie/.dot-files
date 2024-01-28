import abc
import dataclasses

import autoserde

from dofu import specification as sp


@dataclasses.dataclass
class PackageManager(autoserde.Serdeable, abc.ABC):
    @abc.abstractmethod
    def install(self, spec: sp.PackageSpecification):
        pass

    @abc.abstractmethod
    def uninstall(self, spec: sp.PackageSpecification):
        pass

    @abc.abstractmethod
    def update(self, spec: sp.PackageSpecification):
        pass

    @abc.abstractmethod
    def is_available(self) -> bool:
        return False

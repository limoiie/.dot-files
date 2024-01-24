import abc
import dataclasses


@dataclasses.dataclass
class PackageManager(abc.ABC):
    @abc.abstractmethod
    def install(self, package) -> bool:
        pass

    @abc.abstractmethod
    def uninstall(self, package) -> bool:
        pass

    @abc.abstractmethod
    def update(self, package):
        pass

    @abc.abstractmethod
    def is_available(self) -> bool:
        return False

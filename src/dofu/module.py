import dataclasses
import functools
import inspect
import typing as t

import networkx as nx

from dofu import env, requirements, undoable_command as uc, version_control as vc


@dataclasses.dataclass
class ModuleRegistrationMetaInfo:
    """
    Meta registration information of a module.

    This class is used to store the meta registration information of a module.
    """

    # name of the module
    name: str

    def __hash__(self):
        """
        Make the meta info hashable.
        """
        return hash(self.name)


@t.final
class ModuleRegistrationManager:
    """
    Manager of module registration.

    This class is used to manage the registration of modules.
    It provides method to validate the registration and
    resolve the blueprint of the modules to equip.
    """

    # __registry: t.Dict[t.Type["Module"], ModuleRegistrationMetaInfo] = {}
    # """
    # Registry center of all modules.
    # """

    __graph: nx.DiGraph = nx.DiGraph()
    """
    Dependency graph of the modules.
    
    Each node in the graph is a module.
    Each edge in the graph indicates that the source depends on the target.
    """

    @classmethod
    def module(cls, name: str, *, requires: t.List[t.Type["Module"]] = None):
        """
        Register a module to the registry.

        All the registered modules are available to be equipped by the user.
        The user can choose to equip by specifying a list of registered module names.

        :param name: name of the module, should be unique.
            This name will be used to identify the module.
        :param requires: list of modules that this module depends on.
            Each module in the list should be the class of the module.
        :return: decorator
        """

        def decorator(clazz: t.Type["Module"]):
            clazz._name = name
            cls.__graph.add_node(clazz, meta=ModuleRegistrationMetaInfo(name=name))
            for required in requires or []:
                cls.__graph.add_edge(clazz, required)
            return clazz

        return decorator

    @classmethod
    def validate(cls):
        """
        Validate the registration.

        This method will check:
        - whether all modules required by a module are registered
        - whether there is a cycle in the dependency graph of the modules

        This method will be called in the src/modules/__init__.py file automatically
        after registration and before equipping modules.

        :raises ValueError: if there is a problem in the registry
        """
        # check whether all modules required by a module are registered
        for module in cls.__graph.nodes:
            if cls.__graph[module].get("meta", None) is None:
                raise ValueError(f"module {module} is not registered")

        # check whether there is a cycle in the dependency graph
        dependency_cycle = nx.find_cycle(cls.__graph)
        if dependency_cycle:
            raise ValueError(f"dependency cycle detected: {dependency_cycle}")

    @classmethod
    def resolve_equip_blueprint(
        cls, module_names: t.List[str]
    ) -> t.List[t.Type["Module"]]:
        """
        Resolve the blueprint of the modules to equip.

        This method creates a blueprint to indicating the equip order of the modules,
        where all dependencies are equipped before each module.
        It will achieve this by following steps:
        1. validate the module names;
        2. collect all the required modules;
        3. sort the modules topologically.

        :param module_names: list of module names.
            The order of the list is not important
            because the order will be resolved automatically
            to make sure all dependencies are equipped before each module.
        :return: blueprint of the modules to equip.
        """
        modules = set(map(cls.module_class_by_name, module_names))
        completed_modules = functools.reduce(
            set.union,
            # since the edge indicates dependency, all descendants are required by it
            map(lambda module: nx.descendants(cls.__graph, module), modules),
            modules,
        )

        sorted_modules = reversed(list(nx.topological_sort(cls.__graph)))
        sorted_completed_modules = [
            module for module in sorted_modules if module in completed_modules
        ]

        return sorted_completed_modules

    @classmethod
    def resolve_remove_blueprint(
        cls, module_names: t.List[str]
    ) -> t.List[t.Type["Module"]]:
        """
        Resolve the blueprint of the modules to be removed.

        This method creates a blueprint to indicating the remove order of the modules,
        where each module is removed only if no other module depends on it.
        It will achieve this by following steps:
        1. validate the module names;
        2. collect all the modules to remove;
        3. sort the modules topologically.

        :param module_names: list of module names.
            The order of the list is not important
            because the order will be resolved automatically
            to make sure each module is removed only if no other module depends on it.
        :return: blueprint of the modules to remove.
        """

        modules = set(map(cls.module_class_by_name, module_names))
        completed_modules = functools.reduce(
            set.union,
            # since the edge indicates dependency, all ancestors requires it
            map(lambda module: nx.ancestors(cls.__graph, module), modules),
            modules,
        )

        sorted_modules = nx.topological_sort(cls.__graph)
        sorted_completed_modules = [
            module for module in sorted_modules if module in completed_modules
        ]

        return sorted_completed_modules

    @classmethod
    def module_class_by_name(cls, name: str) -> t.Type["Module"]:
        """
        Get the module class by its name.

        :param name: name of the module.
        :return: class of the module.
        """
        for module, attrs in cls.__graph.nodes.items():
            if attrs["meta"].name == name:
                return module

        raise ValueError(f"module {name} is not registered")

    @classmethod
    def module_meta_by_name(cls, name: str) -> t.Type[ModuleRegistrationMetaInfo]:
        """
        Get the module meta by its name.

        :param name: name of the module.
        :return: class of the module.
        """
        for _, attrs in cls.__graph.nodes.items():
            if attrs["meta"].name == name:
                return attrs["meta"]

        raise ValueError(f"module {name} is not registered")

    @classmethod
    def module_meta(
        cls, module: t.Type["Module"]
    ) -> t.Type[ModuleRegistrationMetaInfo]:
        """
        Get the module meta by its class.

        :param module: class of the module.
        :return: class of the module.
        """
        return cls.__graph.nodes[module]["meta"]


class Module:
    """
    Base class of all modules.

    A module is a collection of tools and configurations.
    Each module is responsible for installing and removing its tools and configurations.
    """

    _name: str
    """
    Name of the module. it will be set by the registration decorator.
    """

    _package_requirements: t.List[requirements.PackageRequirement]
    """
    List of required packages, most of them are tools.
    """

    _git_repo_requirements: t.List[requirements.GitRepoRequirement]
    """
    List of required git repos, most of them are configurations.
    """

    _config_steps: t.List[uc.UndoableCommand]
    """
    List of steps to install or update the configurations.
    """

    @classmethod
    def name(cls):
        return cls._name

    @classmethod
    def package_requirements(cls):
        return cls._package_requirements

    @classmethod
    def git_repo_requirements(cls):
        return cls._git_repo_requirements

    @classmethod
    def config_steps(cls):
        return cls._config_steps

    @classmethod
    def last_commit_id(cls):
        """
        Get the last commit id of the module.

        Currently, the module is completely defined by its class.
        """
        module_path = inspect.getfile(cls)
        return vc.last_commit_id_of(repo_path=env.project_root(), path=module_path)

    module = ModuleRegistrationManager.module

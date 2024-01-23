import dataclasses
import inspect
import typing as t

from dofu import env, requirements, undoable_command as uc, version_control as vc


@dataclasses.dataclass
class ModuleRegistrationMetaInfo:
    """
    Meta registration information of a module.

    This class is used to store the meta registration information of a module.
    """

    # name of the module
    name: str

    # class of the module
    clazz: t.Type["Module"]

    # list of modules that this module depends on
    requires: t.List[t.Type["Module"]]

    def __hash__(self):
        return hash(self.clazz)


class ModuleRegistrationManager:
    """
    Manager of module registration.

    This class is used to manage the registration of modules.
    It provides method to validate the registration and
    resolve the blueprint of the modules to equip.
    """

    __registry: t.Dict[t.Type["Module"], ModuleRegistrationMetaInfo] = {}
    """
    Registry center of all modules.
    """

    @staticmethod
    def module(name: str, *, requires: t.List[t.Type["Module"]] = None):
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
            ModuleRegistrationManager.__registry[clazz] = ModuleRegistrationMetaInfo(
                name=name, clazz=clazz, requires=requires or []
            )
            return clazz

        return decorator

    @staticmethod
    def validate():
        """
        Validate the registration.

        This method will check:
        - whether all modules required by a module are registered
        - whether there is a cycle in the dependency graph of the modules

        This method will be called in the src/modules/__init__.py file automatically
        after registration and before equipping modules.

        :raises ValueError: if there is a problem in the registry
        """
        for meta in ModuleRegistrationManager.__registry.values():
            for required in meta.requires:
                if required not in ModuleRegistrationManager.__registry:
                    raise ValueError(
                        f"module {meta.name} requires {required} but it is not registered"
                    )

        # todo: check if there is a cycle in the dependency graph

    @staticmethod
    def resolve_equip_blueprint(module_names: t.List[str]) -> t.List[t.Type["Module"]]:
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

        modules_to_equip = set()
        # collect all modules to equip and all modules required by them
        while module_names:
            name = module_names.pop()
            meta = ModuleRegistrationManager.module_meta_by_name(name)
            modules_to_equip.add(meta.clazz)
            for required in meta.requires:
                if required not in modules_to_equip:
                    modules_to_equip.add(required)
                    module_names.append(required.name())

        be_required_graph = {}  # map module to a set of modules requiring it
        requiring_count = {}  # map module to the number of modules it requires
        # build dependency graph and dependency count
        for clazz in modules_to_equip:
            requiring_count.setdefault(clazz, 0)
            for required in ModuleRegistrationManager.__registry[clazz].requires:
                be_required_graph.setdefault(required, set()).add(clazz)
                requiring_count[clazz] += 1

        modules_to_equip_sorted = []
        # topological sort modules to schedule the order to equip them
        while modules_to_equip:
            for clazz in modules_to_equip:
                if requiring_count[clazz] == 0:  # 0 means all its dependencies are met
                    modules_to_equip.remove(clazz)
                    modules_to_equip_sorted.append(clazz)
                    for requiring in be_required_graph.get(clazz, []):
                        requiring_count[requiring] -= 1
                    break

            else:
                raise RuntimeError("dependency cycle detected")

        return modules_to_equip_sorted

    @staticmethod
    def resolve_remove_blueprint(module_names: t.List[str]) -> t.List[t.Type["Module"]]:
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

        modules_to_remove = set()
        while module_names:
            name = module_names.pop()
            meta = ModuleRegistrationManager.module_meta_by_name(name)
            modules_to_remove.add(meta.clazz)

        requiring_graph = {}  # map module to a set of modules it depends on
        be_required_count = {}  # map module to the number of modules depend on it
        for clazz in modules_to_remove:
            requiring_graph.setdefault(clazz, set()).update(
                ModuleRegistrationManager.__registry[clazz].requires
            )
            for required in ModuleRegistrationManager.__registry[clazz].requires:
                be_required_count.setdefault(required, 0)
                be_required_count[required] += 1

        modules_to_remove_sorted = []
        while modules_to_remove:
            for clazz in modules_to_remove:
                if be_required_count[clazz] == 0:  # 0 means no one depends on it
                    modules_to_remove.remove(clazz)
                    modules_to_remove_sorted.append(clazz)
                    for requiring in requiring_graph.get(clazz, []):
                        be_required_count[requiring] -= 1
                    break

            else:
                raise RuntimeError("dependency cycle detected")

        return modules_to_remove_sorted

    @staticmethod
    def module_class_by_name(name: str) -> t.Type["Module"]:
        """
        Get the module class by its name.

        :param name: name of the module.
        :return: class of the module.
        """
        return ModuleRegistrationManager.module_meta_by_name(name).clazz

    @staticmethod
    def module_meta_by_name(name: str) -> t.Type[ModuleRegistrationMetaInfo]:
        """
        Get the module meta by its name.

        :param name: name of the module.
        :return: class of the module.
        """
        for meta in ModuleRegistrationManager.__registry.values():
            if meta.name == name:
                return meta

        raise ValueError(f"module {name} is not registered")

    @staticmethod
    def module_meta(module: t.Type["Module"]) -> t.Type[ModuleRegistrationMetaInfo]:
        """
        Get the module meta by its class.

        :param module: class of the module.
        :return: class of the module.
        """
        return ModuleRegistrationManager.__registry[module]


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

import contextlib
import dataclasses
import enum
import functools
import itertools
import logging
import os
import typing as t

import autoserde

from dofu import (
    env,
    module as m,
    package_manager as pm,
    requirement as req,
    shutils,
    undoable_command as uc,
    utils,
)

_logger = logging.getLogger(__name__)


@dataclasses.dataclass
class PackageInstallationMetaInfo:
    """
    Meta information about the installation of a package.
    """

    requirement: req.PackageRequirement
    """
    The requirement of the package that is installed.
    """

    manager: t.Optional[pm.PackageManager]
    """
    The manager has been used to install the package.
    """

    used_existing: bool
    """
    Whether the package has been installed before.
    """


@dataclasses.dataclass
class GitRepoInstallationMetaInfo:
    """
    Meta information about the installation of a git repository.
    """

    requirement: req.GitRepoRequirement
    """
    The requirement of the git repository that is installed.
    """

    used_existing: bool
    """
    Whether the repo has been cloned before.
    """


@autoserde.serdeable
class ModuleEquipmentStatus(enum.Enum):
    """
    Status of a module installation.
    """

    PRISTINE = enum.auto()
    """
    The module is not installed.
    """

    INSTALLED = enum.auto()
    """
    The module is installed.
    """

    REMOVED = enum.auto()
    """
    The module is removed.
    """

    BROKEN = enum.auto()
    """
    The module is broken during installing or removing.
    """


@autoserde.serdeable
class ModuleEquipmentTransactionStatus(enum.Enum):
    """
    Status of a module equipment transaction.
    """

    PRISTINE = enum.auto()
    """
    The transaction is not started.
    """

    STARTED = enum.auto()
    """
    The transaction is started.
    """

    COMMITTED = enum.auto()
    """
    The transaction is committed.
    """

    ROLLED_BACK = enum.auto()
    """
    The transaction is rolled back.
    """

    FAILED = enum.auto()
    """
    The transaction is failed.
    """

    FAILED_ROLLBACK = enum.auto()
    """
    The transaction is failed during rollback.
    """


@dataclasses.dataclass
class ModuleEquipmentTransaction(contextlib.AbstractContextManager):
    """
    Module equipment transaction.
    """

    commit_id: str
    """
    Hashcode of the commit where the transaction was started.
    """

    records: t.List[uc.UndoableCommand] = dataclasses.field(default_factory=list)
    """
    List of executed undoable commands.
    """

    status: ModuleEquipmentTransactionStatus = ModuleEquipmentTransactionStatus.PRISTINE
    """
    Status of the module before the transaction.
    """

    rollback_cursor: int = -1
    """
    Cursor of the records, indicating the index of the last rollback command.
    """

    def __enter__(self):
        self.records = []
        self.status = ModuleEquipmentTransactionStatus.STARTED
        return self

    def __exit__(self, __exc_type, __exc_value, __traceback):
        if __exc_type is None:
            self.status = ModuleEquipmentTransactionStatus.COMMITTED

        else:  # __exc_type is not None means the transaction is failed
            self.status = ModuleEquipmentTransactionStatus.FAILED
            self.rollback()

    @property
    def len(self):
        """
        Length of the records.
        """
        return len(self.records)

    @property
    def effect_len(self):
        """
        Length of the effect records.
        """
        return len(self.records) if self.rollback_cursor == -1 else self.rollback_cursor

    @property
    def effect_records(self):
        """
        Get the effect records of the transaction.
        """
        return self.records[: self.effect_len]

    def rollback(self):
        """
        Rollback the transaction.
        """
        for _ in self.rollback_lazily():
            pass

    def rollback_lazily(self):
        """
        Rollback the transaction lazily.

        :return: generator of the rollback process.
        """
        self.status = ModuleEquipmentTransactionStatus.ROLLED_BACK
        for i in range(self.effect_len)[::-1]:
            ret = self.records[i].undo()
            if ret is not None and ret.retcode != 0:
                self.status = ModuleEquipmentTransactionStatus.FAILED_ROLLBACK
                _logger.error(f"Failed to rollback command {self.records[i]} - {ret}")

                raise ret.to_error()

            self.rollback_cursor = i
            yield


@dataclasses.dataclass
class ModuleEquipmentMetaInfo:
    """
    Meta information of a module installation.

    This class is used to store the meta information of a module installation.
    """

    module_name: str
    """
    Name of the installed module.
    """

    package_installations: t.List[PackageInstallationMetaInfo]
    """
    List of installed packages, most of them are tools.
    """

    gitrepo_installations: t.List[GitRepoInstallationMetaInfo]
    """
    List of installed git repos, most of them are configurations.
    """

    transactions: t.List[ModuleEquipmentTransaction]
    """
    List of transactions of undoable commands
    which are used to create or update the configurations.
    """

    status: ModuleEquipmentStatus = ModuleEquipmentStatus.PRISTINE
    """
    Whether the module is installed.
    """

    @property
    def installed(self):
        """
        Whether the module is installed.
        """
        return self.status == ModuleEquipmentStatus.INSTALLED

    @property
    def installed_hashcode(self):
        """
        Hashcode of the commit where the module was installed (first time equipped)
        """
        return self.transactions[0].commit_id if self.transactions else None

    @property
    def updated_hashcode(self):
        """
        Hashcode of the commit where the module was updated (last time equipped)
        """
        return self.transactions[-1].commit_id if self.transactions else None

    @contextlib.contextmanager
    def transaction(self):
        """
        Create a new transaction for applying undoable commands.
        """
        clazz = m.ModuleRegistrationManager.module_class_by_name(self.module_name)
        with ModuleEquipmentTransaction(clazz.last_commit_id()) as transaction:
            try:
                yield transaction

            finally:
                if transaction.records:  # append only non-empty transaction
                    self.transactions.append(transaction)

    @property
    def len_commands(self):
        """
        Get the number of commands to apply the config patches.
        """
        return sum(transaction.effect_len for transaction in self.transactions)

    def commands(self):
        """
        Get the commands to apply the config patches.
        """
        for transaction in self.transactions:
            yield from transaction.effect_records

    def rollback(self):
        """
        Rollback the commands one by one.
        """
        for _ in self.rollback_lazily():
            pass

    def rollback_lazily(self):
        """
        Rollback the commands one by one lazily.

        :return: generator of the rollback process.
        """
        for transaction in reversed(self.transactions):
            yield from transaction.rollback_lazily()


@dataclasses.dataclass
class ModuleEquipmentManager:
    """
    Manager of module equipment.

    This class is used to manage the installation of modules.
    """

    meta: t.Dict[str, ModuleEquipmentMetaInfo] = dataclasses.field(default_factory=dict)

    @staticmethod
    @functools.cache
    def load() -> "ModuleEquipmentManager":
        """
        Load the meta information from the persistence file.
        """
        config_path = env.equipment_persistence_file()
        if not os.path.isfile(config_path):
            return ModuleEquipmentManager()

        options = autoserde.Options(recursively=True, strict=True)
        return autoserde.AutoSerde.deserialize(
            config_path, cls=ModuleEquipmentManager, options=options, fmt="yaml"
        )

    def save(self):
        """
        Save the meta information to the configuration file.
        """
        config_path = env.equipment_persistence_file()
        with shutils.file_update_guarder(config_path) as tmp_path:
            options = autoserde.Options(recursively=True, strict=True, with_cls=True)
            autoserde.AutoSerde.serialize(
                self, tmp_path, options=options, fmt="yaml", sort_keys=False
            )

    def equipped_module_names(self):
        """
        Get the names of the equipped modules.
        """
        return [meta.module_name for meta in self.meta.values()]

    def _equipment_meta(self, module_name: str) -> ModuleEquipmentMetaInfo:
        """
        Get the meta information of an equipped module.

        :param module_name: name of the module to get.
        :return: meta information of the module.
        """
        return self.meta.get(module_name, None) or ModuleEquipmentMetaInfo(
            module_name=module_name,
            package_installations=[],
            gitrepo_installations=[],
            transactions=[],
        )

    def sync(self, module_names: t.List[str]):
        """
        Sync the modules.

        This method will equip the given modules and the modules they depend on.
        What's more, the modules that are not required any more will be removed.

        The order of the modules is not important
        as the order will be resolved automatically
        to make sure that each module is equipped after its dependencies are equipped.

        :param module_names: list of module names.
        """
        blueprint = m.ModuleRegistrationManager.resolve_equip_blueprint(module_names)
        remove_blueprint = m.ModuleRegistrationManager.resolve_remove_blueprint(
            set(self.meta) - set(module.name() for module in blueprint)
        )

        try:
            self._remove_modules(remove_blueprint)
            self._equip_modules(blueprint)

        finally:
            self.save()

    def remove(self, module_names: t.List[str]):
        """
        Remove the modules.

        This method will remove the given modules and the modules they depend on.

        The order of the modules is not important
        as the order will be resolved automatically
        to make sure that each module is removed after its dependencies are removed.

        :param module_names: list of module names.
        """
        blueprint = m.ModuleRegistrationManager.resolve_remove_blueprint(module_names)

        try:
            self._remove_modules(blueprint)

        finally:
            self.save()

    def equip(self, module_names: t.List[str]):
        """
        Equip the modules.

        This method will equip the given modules and the modules they depend on.

        The order of the modules is not important
        as the order will be resolved automatically
        to make sure that each module is equipped after its dependencies are equipped.

        :param module_names: list of module names.
        """
        blueprint = m.ModuleRegistrationManager.resolve_equip_blueprint(module_names)

        try:
            self._equip_modules(blueprint)

        finally:
            self.save()

    def _remove_modules(self, blueprint):
        """
        Remove modules.

        :param blueprint: A list of modules to remove sorted topologically.
        """
        _logger.info(
            f"{len(blueprint)} modules to be removed"
            f" - {[module.name() for module in blueprint]}"
        )

        # remove modules that are not required any more
        for module in blueprint:
            _logger.info(f"Removing module {module.name()}")

            meta = self._equipment_meta(module.name())
            try:
                self._remove_one_step(meta)
                meta.status = ModuleEquipmentStatus.REMOVED
                _logger.info(f"Removed!")

            except Exception:
                meta.status = ModuleEquipmentStatus.BROKEN
                _logger.error(f"Failed to remove Module {module.name()}")
                raise

            else:  # remove the meta only if the module is removed successfully
                del self.meta[meta.module_name]

    def _equip_modules(self, blueprint: t.List[t.Type["m.Module"]]):
        """
        Equip modules.

        :param blueprint: A list of modules to equip sorted topologically.
        :return:
        """
        _logger.info(
            f"{len(blueprint)} modules to be equipped"
            f" - {[module.name() for module in blueprint]}"
        )

        # equip modules that are required
        for module in blueprint:
            _logger.info(f"Synchronizing module {module.name()}")

            meta = self._equipment_meta(module.name())
            try:
                self._equip_one_step(module, meta)
                meta.status = ModuleEquipmentStatus.INSTALLED
                _logger.info(f"Equipped!")

            except Exception:
                meta.status = ModuleEquipmentStatus.BROKEN
                _logger.error(f"Failed to equip Module {module.name()}")
                raise

            finally:  # save the meta even if the module is broken
                self.meta[meta.module_name] = meta

    def _equip_one_step(
        self, module: t.Type["m.Module"], meta: ModuleEquipmentMetaInfo
    ):
        """
        Equip a module.

        This method is just one step of the whole equip process.
        It assumes that all the dependencies of the module have been equipped.
        To equip a module, please use the `equip` method.

        :param module: module to equip.
        :param meta: equipment meta info of the module.
        """
        self._sync_packages_step(module, meta)
        self._sync_gitrepos_step(module, meta)
        self._sync_commands_step(module, meta)

    @staticmethod
    def _sync_packages_step(module: t.Type["m.Module"], meta: ModuleEquipmentMetaInfo):
        """
        Sync package requirements.

        This method will install all the required packages if they are not installed,
        and remove all the installed packages if they are not required any more.
        """
        # sync already installed
        for installation in list(meta.package_installations):
            _logger.info(
                f"Syncing installed package"
                f" - {_repr_pkg_requirement(installation.requirement)}"
            )

            required = utils.find(
                module.package_requirements(),
                value=installation.requirement,
                default=None,
            )

            # not required any more, remove the installation
            if required is None or not installation.requirement.is_satisfied():
                _logger.debug(f" - package is not required any more, uninstalling it")

                if not installation.used_existing and installation.manager:
                    installation.requirement.uninstall(installation.manager)
                meta.package_installations.remove(installation)

        # install packages that are required but not installed
        for requirement in module.package_requirements():
            _logger.info(
                f"Equipping package" f" - {_repr_pkg_requirement(requirement)}"
            )

            installation = utils.find(
                meta.package_installations,
                pred=lambda x: x.requirement == requirement,
                default=None,
            )

            # installed already
            if installation is not None:
                _logger.debug(f" - reinstall package since having been installed")

                if not requirement.is_satisfied():
                    _logger.warning(f" - reinstalling package as seemed broken")

                    # reinstall since the package is broken
                    installation.manager = requirement.install()
                    installation.used_existing = False
                else:
                    _logger.debug(f" - updating package...")

                    # update?
                    # Currently, the installed package with different version will
                    # be uninstalled and reinstalled with the new version. It seems
                    # that there is no need to run update again.
                    pass

            # install for the first time
            else:
                if not requirement.is_satisfied():
                    _logger.debug(f" - installing package")

                    # install if the package is not installed
                    manager = requirement.install()
                    used_existing = False
                else:
                    _logger.debug(f" - using existing package installed by other")

                    manager = None
                    used_existing = True

                meta.package_installations.append(
                    PackageInstallationMetaInfo(
                        requirement=requirement,
                        manager=manager,
                        used_existing=used_existing,
                    )
                )

    @staticmethod
    def _sync_gitrepos_step(module: t.Type["m.Module"], meta: ModuleEquipmentMetaInfo):
        """
        Sync git repo requirements.

        This method will clone all the required git repos if they are not cloned,
        and remove all the cloned git repos if they are not required any more.
        """

        # sync already installed
        for installation in list(meta.gitrepo_installations):
            _logger.info(
                f"Syncing cloned gitrepo"
                f" - {_repr_git_requirement(installation.requirement)}"
            )

            required = utils.find(
                module.gitrepo_requirements(),
                value=installation.requirement,
                key=lambda x: x.url,
                default=None,
            )

            # not required any more or broken, remove the installation
            if required is None or not installation.requirement.is_satisfied():
                _logger.debug(f" - removing gitrepo as not being required any more")

                installation.requirement.uninstall()
                meta.gitrepo_installations.remove(installation)

            # required but the local path has changed, move to the new dst
            elif required.path != installation.requirement.path:
                _logger.debug(f" - moving gitrepo to new dst {required.path}")

                shutils.move(installation.requirement.path, required.path)
                installation.requirement.path = required.path

        # install requirements that are required but not installed
        for requirement in module.gitrepo_requirements():
            _logger.info(f"Equipping gitrepo - {_repr_git_requirement(requirement)}")

            installation = utils.find(
                meta.gitrepo_installations,
                pred=lambda x: x.requirement.url == requirement.url,
                default=None,
            )

            # installed already
            if installation is not None:
                if not requirement.is_satisfied():
                    _logger.warning(f" - re-cloning gitrepo as seemed broken")

                    # reinstall since the gitrepo is broken
                    requirement.install()
                    installation.used_existing = False
                else:
                    _logger.debug(f" - updating existing gitrepo")

                    requirement.update()

            # install for the first time
            else:
                if not requirement.is_satisfied():
                    _logger.debug(f" - cloning gitrepo")

                    # install if the package is not installed
                    requirement.install()
                    used_existing = False
                else:
                    _logger.debug(f" - using existing gitrepo")

                    used_existing = True

                meta.gitrepo_installations.append(
                    GitRepoInstallationMetaInfo(
                        requirement=requirement,
                        used_existing=used_existing,
                    )
                )

    @staticmethod
    def _sync_commands_step(module: t.Type["m.Module"], meta: ModuleEquipmentMetaInfo):
        """
        Sync undoable commands sequences.

        This method will keep the common prefix steps,
        and undo all the executed steps after the common prefix steps.
        Then, it will execute the remaining steps.
        """
        _logger.info(f"Syncing commands")

        itr_installed_cmds = iter(meta.commands())
        itr_required_cmds = iter(module.command_requirements())
        for installed, required in zip(itr_installed_cmds, itr_required_cmds):
            # skip the foremost steps that have been executed by checking spec identity
            if installed.spec_tuple() != required.spec_tuple():
                itr_installed_cmds = itertools.chain([installed], itr_installed_cmds)
                itr_required_cmds = itertools.chain([required], itr_required_cmds)
                break

        _logger.debug(f" - rolling back withdrawn config commands if any")

        # rollback the executed commands after index i
        for _ in zip(itr_installed_cmds, meta.rollback_lazily()):
            pass

        _logger.debug(f" - executing new config commands if any")

        # execute the remaining configuring commands
        with meta.transaction() as transaction:
            for command in itr_required_cmds:
                ret = command.exec()
                if ret.retcode != 0:
                    raise ret.to_error()

                transaction.records.append(command)

    @staticmethod
    def _remove_one_step(meta: ModuleEquipmentMetaInfo):
        """
        Remove a module.

        :param meta: equipment meta info of the module.
        """
        _logger.info("Rolling back config command transactions")

        # undo commands
        while meta.transactions:
            meta.transactions[-1].rollback()
            meta.transactions.pop()

        _logger.info("Removing gitrepos")

        # remove gitrepos
        while meta.gitrepo_installations:
            meta.gitrepo_installations[-1].requirement.uninstall()
            meta.gitrepo_installations.pop()

        _logger.info("Uninstalling packages")

        # uninstall packages
        while meta.package_installations:
            meta.package_installations[-1].requirement.uninstall(
                meta.package_installations[-1].manager
            )
            meta.package_installations.pop()


def _repr_pkg_requirement(requirement: req.PackageRequirement):
    return f"{requirement.spec.package}:{requirement.spec.version}"


def _repr_git_requirement(requirement: req.GitRepoRequirement):
    return f'{requirement.url}@{requirement.branch or "main"}'

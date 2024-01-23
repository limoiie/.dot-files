import contextlib
import dataclasses
import enum
import functools
import os
import shutil
import typing as t

import autoserde

from dofu import env, requirements, undoable_command as uc, utils
from dofu.module import Module, ModuleRegistrationManager


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
    def cursor(self):
        """
        Cursor pointing to the last command rolled back.

        self.rollback_cursor == -1 means no record has been rolled back.
        """
        if self.rollback_cursor == -1:
            return len(self.records)
        return self.rollback_cursor

    @property
    def effect_records(self):
        """
        Get the effect records of the transaction.
        """
        return self.records[: self.rollback_cursor]

    def rollback(self, keeps: int = 0):
        """
        Rollback the transaction.
        """
        self.status = ModuleEquipmentTransactionStatus.ROLLED_BACK
        for i in self.records[keeps : self.cursor : -1]:
            try:
                self.records[i].undo()
                self.rollback_cursor = i

            except Exception:
                self.status = ModuleEquipmentTransactionStatus.FAILED_ROLLBACK
                raise


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

    installed_packages: t.List[requirements.PackageInstallationMetaInfo]
    """
    List of installed packages, most of them are tools.
    """

    installed_git_repos: t.List[requirements.GitRepoInstallationMetaInfo]
    """
    List of installed git repos, most of them are configurations.
    """

    transactions: t.List[ModuleEquipmentTransaction]
    """
    List of transactions of config patches.
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
        Create a new transaction for applying config patches.
        """
        meta = ModuleRegistrationManager.module_meta_by_name(self.module_name)
        with ModuleEquipmentTransaction(meta.clazz.last_commit_id()) as transaction:
            self.transactions.append(transaction)
            yield transaction


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
        with utils.file_update_guarder(config_path):
            options = autoserde.Options(recursively=True, strict=True, with_cls=False)
            autoserde.AutoSerde.serialize(
                self, config_path, options=options, fmt="yaml", sort_keys=False
            )

    def _equipment_meta(self, module_name: str) -> ModuleEquipmentMetaInfo:
        """
        Get the meta information of an equipped module.

        :param module_name: name of the module to get.
        :return: meta information of the module.
        """
        return self.meta.get(module_name, None) or ModuleEquipmentMetaInfo(
            module_name=module_name,
            installed_packages=[],
            installed_git_repos=[],
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
        blueprint = ModuleRegistrationManager.resolve_equip_blueprint(module_names)
        remove_blueprint = ModuleRegistrationManager.resolve_remove_blueprint(
            set(self.meta) - set(map(ModuleRegistrationManager.module_meta, blueprint))
        )
        for module in remove_blueprint:
            meta = self._equipment_meta(module.name())
            # TODO: persistent current state if throw errors?
            self._remove_one_step(meta)
            del self.meta[meta.module_name]

        for module in blueprint:
            meta = self._equipment_meta(module.name())
            # TODO: persistent current state if throw errors?
            self._equip_one_step(module, meta)
            self.meta[meta.module_name] = meta

        self.save()

    def _equip_one_step(self, module: t.Type["Module"], meta: ModuleEquipmentMetaInfo):
        """
        Equip a module.

        This method is just one step of the whole equip process.
        It assumes that all the dependencies of the module have been equipped.
        To equip a module, please use the `equip` method.

        :param module: module to equip.
        :param meta: equipment meta info of the module.
        """
        self._sync_packages_step(module, meta)
        self._sync_git_repos_step(module, meta)
        self._sync_config_files_step(module, meta)

    @staticmethod
    def _sync_packages_step(module: t.Type["Module"], meta: ModuleEquipmentMetaInfo):
        """
        Sync package requirements.

        This method will install all the required packages if they are not installed,
        and remove all the installed packages if they are not required any more.
        """
        # remove packages that are not required any more
        for installed_meta in list(meta.installed_packages):
            if installed_meta.requirement not in module.package_requirements():
                installed_meta.requirement.uninstall(installed_meta.manager)
                meta.installed_packages.remove(installed_meta)

        # install packages that are required but not installed
        for requirement in module.package_requirements():
            if not requirement.is_installed():
                manager = requirement.install()
                if not manager:
                    raise RuntimeError(f"failed to install package {requirement}")
                meta.installed_packages.append(
                    requirements.PackageInstallationMetaInfo(
                        requirement=requirement,
                        manager=manager,
                    )
                )

    @staticmethod
    def _sync_git_repos_step(module: t.Type["Module"], meta: ModuleEquipmentMetaInfo):
        """
        Sync git repo requirements.

        This method will clone all the required git repos if they are not cloned,
        and remove all the cloned git repos if they are not required any more.
        """
        # map repo url to complete requirement
        git_repo_requirements = {
            required.repo: required for required in module.git_repo_requirements()
        }

        for installed_meta in list(meta.installed_git_repos):
            installed = installed_meta.requirement
            # remove installed requirements that are not required any more
            if installed.repo not in git_repo_requirements:
                installed.uninstall()
                meta.installed_git_repos.remove(installed_meta)
                continue

            required = git_repo_requirements[installed.repo]
            # move installed requirements whose paths have changed
            if required.path != installed.path:
                shutil.move(installed.path, required.path)

        # install requirements that are required but not installed
        for requirement in module.git_repo_requirements():
            if not requirement.is_installed():
                requirement.install()
                meta.installed_git_repos.append(
                    requirements.GitRepoInstallationMetaInfo(
                        requirement=requirement,
                    )
                )

    @staticmethod
    def _sync_config_files_step(
        module: t.Type["Module"], meta: ModuleEquipmentMetaInfo
    ):
        """
        Sync config files.

        This method will keep the common prefix steps,
        and undo all the executed steps after the common prefix steps.
        Then, it will execute the remaining steps.
        """
        require_steps = list(module.config_steps())

        # exclude the steps that have been executed by checking the spec tuple identity
        for ti, transaction in enumerate(meta.transactions):
            for ri, rec in enumerate(transaction.records):
                if require_steps and require_steps[0].spec_tuple() == rec.spec_tuple():
                    require_steps.pop(0)
                    continue

                # undo the remaining transactions reversely
                for transaction_to_rollback in meta.transactions[ti + 1 :: -1]:
                    transaction_to_rollback.rollback()
                meta.transactions[ti].rollback(keeps=ri)
                break

        if require_steps:
            # execute the remaining new steps
            with meta.transaction() as transaction:
                for rec in require_steps:
                    ret = rec.exec()
                    if ret.retcode != 0:
                        raise RuntimeError(f"failed to execute command: {ret.cmdline}")

                    transaction.records.append(rec)

    @staticmethod
    def _remove_one_step(meta: ModuleEquipmentMetaInfo):
        """
        Remove a module.

        :param meta: equipment meta info of the module.
        """
        # undo config patches
        while meta.transactions:
            meta.transactions[-1].rollback()
            meta.transactions.pop()

        # remove git repos
        while meta.installed_git_repos:
            meta.installed_git_repos[-1].requirement.uninstall()
            meta.installed_git_repos.pop()

        # uninstall packages
        while meta.installed_packages:
            meta.installed_packages[-1].requirement.uninstall(
                meta.installed_packages[-1].manager
            )
            meta.installed_packages.pop()

import logging
import typing

import fire

from dofu import gum
from dofu.equipment import ModuleEquipmentManager
from dofu.inspect import extend_interface
from dofu.logging import init as init_logging
from dofu.module import ModuleRegistrationManager
from dofu.options import Options, Strategy

_logger = logging.getLogger("dofu.app")


class App:
    """
    Dofu Command Line Interface

    Dofu is a tool for managing dotfiles for limo or anyone else.
    With dofu, you can easily equip, remove, and sync modules
    across different machines, as well as update patches.
    """

    @staticmethod
    def init(
        *,
        dry_run: bool = False,
        strategy: typing.Literal["ask", "force", "auto", "quit"] = "quit",
        loglevel: typing.Literal["debug", "info", "warn", "error", "fatal"] = None,
    ):
        """
        :param dry_run: Dry run mode without changing anything.
        :param strategy: The strategy to use when meeting a destructive command.
            Can be one of "ask", "force", "auto", "quit".
        :param loglevel: The log level.
            Can be one of "debug", "info", "warn", "error", "fatal".
        """
        init_logging(loglevel=loglevel)

        options = Options.instance()
        options.dry_run = dry_run
        options.strategy = Strategy.from_name(strategy)

    @staticmethod
    @extend_interface(init)
    def list(*module_names: str, installed_only: bool = None):
        """
        List modules.

        List all the modules, or the modules with the given names.

        :param module_names: The names of modules to list.
        :param installed_only: Whether to list installed modules only.
        """
        # load module equipment meta information
        manager = ModuleEquipmentManager.load()

        installed_module_names = set(manager.equipped_module_names())
        module_names = module_names or ModuleRegistrationManager.all_module_names()
        blueprint = ModuleRegistrationManager.resolve_equip_blueprint(module_names)

        for module in blueprint:
            is_installed = module.name() in installed_module_names
            if installed_only and not is_installed:
                continue

            _logger.info(
                f"Module {module.name()} " +
                ("[green]Installed[/]" if is_installed else "[red]Not Installed[/red]"),
            )
            _logger.debug("- Requirements: ")

            _logger.debug(f"  - Packages:")
            for pkg in module.package_requirements():
                _logger.debug(f"      {pkg.spec.package}@{pkg.spec.version}")

            _logger.debug(f"  - GitRepos")
            for git in module.gitrepo_requirements():
                _logger.debug(f"      {git.url}")

            _logger.debug(f"  - Commands")
            for cmd in module.command_requirements():
                _logger.debug(f"      {cmd.cmdline()[:40]}")

            _logger.debug(f"--")

    @staticmethod
    @extend_interface(init)
    def equip(*module_names: str):
        """
        Equip modules.

        Equip the modules with the given names.
        If no modules are given, you will be asked to choose modules to equip.
        All the dependencies of the modules will be equipped as well.
        The order of equipping is determined by the dependency graph automatically.

        :param module_names: The names of modules to equip.
        """
        # load module equipment meta information
        manager = ModuleEquipmentManager.load()

        # choose modules to equip
        module_names = (
            gum.choose(
                *ModuleRegistrationManager.all_module_names(),
                header="Choose modules to equip",
                no_limit=True,
                selected=manager.equipped_module_names(),
            )
            .strip()
            .split("\n")
            if not module_names
            else module_names
        )

        module_names = list(filter(None, module_names))
        if module_names:
            manager.equip(module_names)

    @staticmethod
    @extend_interface(init)
    def install(*module_names: str):
        """
        Install modules.

        Similar with equip, but can only choose uninstalled modules.

        Equip the modules with the given names.
        If no modules are given, you will be asked to choose modules to equip.
        All the dependencies of the modules will be equipped as well.
        The order of equipping is determined by the dependency graph automatically.

        :param module_names: The names of modules to equip.
        """
        # load module equipment meta information
        manager = ModuleEquipmentManager.load()

        equipped = set(manager.equipped_module_names())

        # choose modules to equip
        module_names = (
            gum.choose(
                *(
                    module
                    for module in ModuleRegistrationManager.all_module_names()
                    if module not in equipped
                ),
                header="Choose modules to install",
                no_limit=True,
            )
            .strip()
            .split("\n")
            if not module_names
            else module_names
        )

        module_names = list(filter(None, module_names))
        if module_names:
            manager.equip(module_names)

    @staticmethod
    @extend_interface(init)
    def remove(*module_names: str):
        """
        Remove modules.

        Remove the modules with the given names.
        If no modules are given, you will be asked to choose modules to remove.
        All the modules depending on the given modules will be removed as well.
        The order of equipping is determined by the dependency graph automatically.

        :param module_names: The names of modules to equip.
        """
        # load module equipment meta information
        manager = ModuleEquipmentManager.load()

        equipped_module_names = manager.equipped_module_names()
        if not equipped_module_names:
            _logger.warning("No modules have been equipped, quit.")
            return

        # choose modules to equip
        module_names = (
            gum.choose(
                *equipped_module_names,
                header="Choose modules to remove",
                no_limit=True,
            )
            .strip()
            .split("\n")
            if not module_names
            else module_names
        )

        module_names = list(filter(None, module_names))
        if module_names:
            manager.remove(module_names)

    @staticmethod
    @extend_interface(init)
    def sync(*module_names: str):
        """
        Sync modules.

        Remove the modules with the given names.
        If no modules are given, you will be asked to choose modules to sync.
        Any chosen module will be equipped, and any unchosen module will be unequipped.
        All the dependencies of the modules will be equipped/unequipped as well.
        The order of equipping is determined by the dependency graph automatically.

        :param module_names: The names of modules to equip.
        """
        # load module equipment meta information
        manager = ModuleEquipmentManager.load()

        # choose modules to equip
        module_names = (
            gum.choose(
                *ModuleRegistrationManager.all_module_names(),
                header="Choose modules to sync",
                selected=manager.equipped_module_names(),
                no_limit=True,
            )
            .strip()
            .split("\n")
            if not module_names
            else module_names
        )

        module_names = list(filter(None, module_names))
        if module_names:
            manager.sync(module_names)


if __name__ == "__main__":
    fire.Fire(App())

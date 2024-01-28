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

        equipped_module_names = set(manager.equipped_module_names())

        # choose modules to equip
        module_names = (
            gum.choose(
                *(
                    module_name
                    for module_name in ModuleRegistrationManager.all_module_names()
                    if module_name not in equipped_module_names
                ),
                header="Choose modules to equip",
                no_limit=True,
                select_if_one=True,
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
                select_if_one=True,
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

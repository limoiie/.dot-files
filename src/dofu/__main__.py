import fire

from dofu import gum
from dofu.equipment import ModuleEquipmentManager
from dofu.module import ModuleRegistrationManager
from dofu.options import Options, Strategy


def main(
    *module_names: str,
    dry_run: bool = False,
    ask: bool = False,
    force: bool = False,
    quiet: bool = False,
    early_quit: bool = True,
):
    options = Options.instance()
    options.dry_run = dry_run
    options.strategy = Strategy.from_flags(
        interactive=ask, overwrite=force, backup=quiet, cancel=early_quit
    )

    # load module equipment meta information
    manager = ModuleEquipmentManager.load()

    # choose modules to equip
    module_names = gum.choose(
        *ModuleRegistrationManager.all_module_names(),
        header="Choose modules to equip",
        selected=manager.equipped_module_names(),
        no_limit=True,
        select_if_one=True,
    ).strip().split("\n") if not module_names else module_names

    module_names = list(filter(None, module_names))
    if module_names:
        manager.sync(module_names)

    else:
        if gum.confirm("Do you really want to REMOVE all?", default=0):
            manager.sync([])


if __name__ == "__main__":
    fire.Fire(main)

import fire

from dofu import gum
from dofu.equipment import ModuleEquipmentManager
from dofu.module import ModuleRegistrationManager
from dofu.options import Options


def main(*, dry_run: bool = False):
    options = Options.instance()
    options.dry_run = dry_run

    # load module equipment meta information
    manager = ModuleEquipmentManager.load()

    # choose modules to equip
    module_names_str = gum.choose(
        *ModuleRegistrationManager.all_module_names(),
        header="Choose modules to equip",
        selected=manager.equipped_module_names(),
        no_limit=True,
        select_if_one=True
    )
    module_names = [m for m in module_names_str.strip().split("\n") if m]

    if module_names:
        manager.sync(module_names)

    else:
        if gum.confirm("Do you really want to REMOVE all?", default=0):
            manager.sync([])


if __name__ == "__main__":
    fire.Fire(main)

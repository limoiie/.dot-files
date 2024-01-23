import fire

from dofu.equipment import ModuleEquipmentManager
from dofu.options import Options


def main(*, dry_run: bool = False):
    options = Options.instance()
    options.dry_run = dry_run

    modules = input("modules:")
    manager = ModuleEquipmentManager.load()
    manager.sync(modules.split(" "))


if __name__ == "__main__":
    fire.Fire(main)

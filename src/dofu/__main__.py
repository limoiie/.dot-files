import fire

from dofu.equipment import ModuleEquipmentManager


def main():
    modules = input('modules:')
    manager = ModuleEquipmentManager.load()
    manager.equip(modules.split(' '))


if __name__ == '__main__':
    fire.Fire(main)

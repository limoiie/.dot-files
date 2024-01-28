# Dofu

Dofu Command Line Interface

Dofu is a tool for managing dotfiles for limo or anyone else. It allows you to easily equip, remove, and sync modules across different machines, as well as update patches.

## Features

Dofu automatically detects changes in dot-files and applies the necessary patches to match the current environment. You can commit the updates in one place and then apply the changes to multiple PCs with different commit history.

Dofu wraps collections of tool chains as modules, each of which is composed of three components:

- Packages: any package that was supposed to be installed or removed via some packaage managers. By installing packages, new commands will be available. For example, curl and neovim are both packages, they could be installed by package managers apt and bob, respectively. After installing curl and neovim, new command curl and nvim will be availiable in terminal.

- Git repositories: any git repositories required to be enable functionalities. Most of them provide configure frameworks, e.g., NvChad. Some provide additional commands, such as fzf.

- Undoable commands: for tweaking configures. These commands are undoable, which enables Dofu to roll back configuration changes and apply new ones automatically.

Dofu enables selective installation, removal, and synchronization of modules. During installation, existing packages and git repositories are directly applied, while existing configurations are backed up. During uninstallation, the backup is restored, the changes are rolled back, and the effects are replayed. Additionally, any packages and git repositories installed by dofu will be removed, while those applied from existing sources will be preserved.

## Requirements

To run this project, you need git and python>3.10. Additionally, you need [gum](https://github.com/charmbracelet/gum) for a user-friendly experience.

## Installation

You can directly install via pip:

```sh
pip install git+https://github.com/limoiie/.dot-files.git
```

Or, if you want to tweak the details, clone the repository to your preferred location:

```sh
git clone https://github.com/limoiie/.dot-files.git ~/.dofu
```

And then, install it using pip:

```sh
cd ~/.dofu && pip install -e .
```

## Usage

Use the following command to check the basic commands:

```sh
python -m dofu -- --help
```

List available modules:

```sh
python -m dofu list
```


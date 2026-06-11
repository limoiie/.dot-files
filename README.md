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

## Toolchains managed by mise

The rust toolchain (rustup, cargo), the go toolchain, neovim, fzf, and the third-party binaries that used to live in dofu's `cargo-crates` and `go-mods` modules are all managed by [mise](https://mise.jdx.dev/). The full list lives in [`xdg-config/mise/config.toml`](xdg-config/mise/config.toml) and includes:

- `rust`, `go` (the toolchains)
- `neovim`, `fzf`
- `bat`, `eza` (replaces the unmaintained `exa`), `fd`, `procs`, `ripgrep`, `sd` (cargo binaries)
- `lazygit`, `lazydocker`, `gum` (go binaries)

Mise is activated in `common-shrc` / `common-zshrc` via `eval "$(mise activate <shell>)"`, and its shims put every binary on `PATH` automatically. `common-shrc` only needs to register the `gtop` / `dtop` shell aliases for lazygit / lazydocker. The dofu `neovim` module is kept around for the config frameworks (NvChad / AstroNvim / LazyVim) and the custom NvChad config symlink — the dotfile-shaped changes that don't fit a mise `[tools]` entry.

## Requirements

To run this project, you need git, python>=3.10 and [uv](https://docs.astral.sh/uv/). Additionally, you need [gum](https://github.com/charmbracelet/gum) for a user-friendly experience.

## Installation

The recommended way is to install dofu as a uv tool. Clone the repository to your preferred location and install it in editable mode:

```sh
git clone https://github.com/limoiie/.dot-files.git ~/.dofu
uv tool install --editable ~/.dofu
```

This creates an isolated environment for dofu and exposes the `dofu` command globally (typically under `~/.local/bin/dofu`). If that directory is not on your `PATH`, run `uv tool update-shell` once.

You can also install it directly from git without cloning:

```sh
uv tool install git+https://github.com/limoiie/.dot-files.git
```

Note that the git install is not editable, so you cannot tweak the sources locally.

## Usage

Use the following command to check the basic commands:

```sh
dofu --help
```

List available modules:

```sh
dofu list
```

During development, you can also run dofu from a checkout without installing it globally:

```sh
uv run --project ~/.dofu dofu --help
```


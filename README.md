# dofu

DOt Files Utility for managing dotfiles.

dofu equips, removes, and syncs modules across different machines. Each module bundles packages, git repositories, and undoable configuration commands so that your entire environment can be reproduced with a single tool.

## Requirements

- git
- Python >= 3.10
- [uv](https://docs.astral.sh/uv/)
- [mise](https://mise.jdx.dev/) (for toolchain and binary management)
- [gum](https://github.com/charmbracelet/gum) (for interactive prompts)

## Quick start

Clone and run the bootstrap script:

```sh
git clone https://github.com/limoiie/.dot-files.git ~/.dot-files
~/.dot-files/setup.sh
```

This installs mise, sets up toolchains and binaries from `xdg-config/mise/config.toml`, and installs dofu itself as an editable `uv tool`.

## Manual installation

Install dofu as a uv tool in editable mode:

```sh
git clone https://github.com/limoiie/.dot-files.git ~/.dofu
uv tool install --editable ~/.dofu
```

The `dofu` command will be available under `~/.local/bin/dofu`. If that directory is not on your `PATH`, run `uv tool update-shell` once.

You can also install directly from git (not editable):

```sh
uv tool install git+https://github.com/limoiie/.dot-files.git
```

During development, run dofu from a checkout without installing globally:

```sh
uv run --project ~/.dofu dofu --help
```

## Global options

Every subcommand accepts these flags:

| Flag | Values | Default | Description |
|------|--------|---------|-------------|
| `--dry-run` | | `False` | Log what would happen without making changes |
| `--strategy` | `ask`, `force`, `auto`, `quit` | `ask` | How to handle destructive operations |
| `--loglevel` | `debug`, `info`, `warn`, `error`, `fatal` | `info` | Log verbosity |

## Commands

### `dofu equip [module...]`

Equip modules. If no module names are given, an interactive `gum choose` menu lets you select modules. Dependencies are resolved and equipped in topological order.

```sh
dofu equip zsh tmux
```

### `dofu install [module...]`

Like `equip`, but the interactive menu only shows modules that are not yet installed.

```sh
dofu install neovim
```

### `dofu remove [module...]`

Remove modules. Dependents are removed together in reverse dependency order. The interactive menu only shows currently equipped modules.

```sh
dofu remove emacs
```

### `dofu sync [module...]`

Sync modules: chosen modules are equipped, unchosen modules (that were previously equipped) are removed. The interactive menu pre-selects currently equipped modules.

```sh
dofu sync
```

### `dofu list [module...]`

List modules and their requirements. Use `--installed-only` to filter to equipped modules only.

```sh
dofu list --installed-only
```

### `dofu integrate`

Installs dofu as a uv tool in editable mode from the current checkout, making the `dofu` command globally available.

```sh
dofu integrate
```

## Modules

### zsh

Installs zsh, clones [zplug](https://github.com/zplug/zplug), changes the default shell to zsh, and sources `common-shrc` and `common-zshrc` from `~/.zshrc`.

### tmux

Clones [oh-my-tmux](https://github.com/gpakosz/.tmux) and symlinks `tmux.conf` and `tmux.conf.local` into `$XDG_CONFIG_HOME/tmux`.

### neovim

Clones [NvChad](https://github.com/NvChad/NvChad), [AstroNvim](https://github.com/AstroNvim/AstroNvim), and [LazyVim](https://github.com/LazyVim/starter) config frameworks, then symlinks the custom NvChad config. The neovim binary itself is managed by mise, not dofu.

### emacs

Installs emacs, clones [Spacemacs](https://github.com/syl20bnr/spacemacs) and custom layers.

## How modules work

Each module is composed of three kinds of requirements:

- **Packages** — installed or removed via platform-specific package managers (apt, brew, pacman, yum, chocolatey, scoop, cargo, or curl-sh).
- **Git repositories** — cloned to provide config frameworks (e.g. NvChad, oh-my-tmux) or additional commands.
- **Undoable commands** — idempotent configuration patches (symlinks, env var exports, line appends, etc.) that can be rolled back when a module is removed.

During equipping, existing packages and git repos are applied directly, while existing configurations are backed up. During removal, backups are restored, changes are rolled back, and packages/repos installed by dofu are cleaned up — pre-existing items are preserved.

## Toolchains managed by mise

The rust and go toolchains, neovim, fzf, and the third-party binaries that used to live in dofu's `cargo-crates` and `go-mods` modules are all managed by [mise](https://mise.jdx.dev/). The full list lives in [`xdg-config/mise/config.toml`](xdg-config/mise/config.toml) and includes:

- `rust`, `go` (toolchains)
- `neovim`, `fzf`
- `bat`, `eza`, `fd`, `procs`, `ripgrep`, `sd` (cargo binaries)
- `lazygit`, `lazydocker`, `gum` (go binaries)

Mise is activated in `common-shrc` / `common-zshrc` via `eval "$(mise activate <shell>)"`, and its shims put every binary on `PATH` automatically. The dofu `neovim` module only owns the config frameworks (NvChad / AstroNvim / LazyVim) and the custom NvChad config symlink — dotfile-shaped changes that don't fit a mise `[tools]` entry.

## Dependencies

- [rich](https://github.com/Textualize/rich) — terminal formatting
- [fire](https://github.com/google/python-fire) — CLI framework
- [pyyaml](https://pyyaml.org/) — YAML persistence
- [python-dotenv](https://github.com/theskumar/python-dotenv) — environment file loading
- [networkx](https://networkx.org/) — dependency graph resolution
- [autoserde](https://github.com/limoiie/autoserde) — serialization

## License

MIT — see [LICENSE](LICENSE).

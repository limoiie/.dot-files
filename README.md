# dotfiles

Personal dotfiles for macOS / Linux / Windows, managed with [chezmoi](https://www.chezmoi.io/).

The repository doubles as chezmoi's source directory using the conventional layout: the source state (files with `dot_`/`dot_config` prefixes) lives at the repository root, and non-dotfile content (this README, `windows/`, `resources/`) is excluded via [`.chezmoiignore`](.chezmoiignore). Shell helper scripts are managed as [dot_local/bin](dot_local/bin) targets (`~/.local/bin`, already on `PATH`).

Tools and toolchains are installed by [mise](https://mise.jdx.dev/) from [`dot_config/mise/config.toml`](dot_config/mise/config.toml).

## Quick start

macOS / Linux:

```sh
git clone https://github.com/limoiie/.dot-files.git ~/.dot-files
~/.dot-files/setup.sh
```

Windows: run `windows/setup.ps`.

`setup.sh` installs mise and chezmoi, clones the repo to `~/.dot-files`, points chezmoi's source directory at it (`ln -s ~/.dot-files ~/.local/share/chezmoi`), applies the dotfiles, and runs `mise install`.

## What chezmoi manages

| Target | Source |
| --- | --- |
| `~/.zshrc`, `~/.shrc` | `dot_zshrc`, `dot_shrc` |
| `~/.vimrc`, `~/.ideavimrc` | `dot_vimrc`, `dot_ideavimrc` |
| `~/.spacemacs` *(only when emacs is enabled)* | `dot_spacemacs` |
| `~/.config/git/*` | `dot_config/git/*` |
| `~/.config/tmux/*` | `dot_config/tmux/*` |
| `~/.config/zellij/*` | `dot_config/zellij/*` |
| `~/.config/NvChad/*` | `dot_config/NvChad/*` |
| `~/.config/kitty/*` | `dot_config/kitty/*` |
| `~/.config/mise/*` | `dot_config/mise/*` |

External git repos, cloned and updated by chezmoi on every apply (see [`.chezmoiexternal.toml`](.chezmoiexternal.toml)):

- [zplug](https://github.com/zplug/zplug) → `~/.config/zplug`
- [oh-my-tmux](https://github.com/gpakosz/.tmux) → `~/.config/oh-my-tmux`
- [Spacemacs](https://github.com/syl20bnr/spacemacs) → `~/.emacs.d` *(only when emacs is enabled)*
- [limo-spacemacs-layers](https://github.com/limoiie/limo-spacemacs-layers) → `~/.emacs.d/private/layers` *(only when emacs is enabled)*

## Optional: emacs / Spacemacs

The emacs setup (Spacemacs, the custom layers, and `~/.spacemacs`) is opt-in. It is disabled by default (see [`.chezmoidata.toml`](.chezmoidata.toml)) and enabled per machine:

```sh
chezmoi edit-config   # add the following, then save:
```

```toml
[data]
emacs = true
```

```sh
chezmoi apply
```

The `emacs` package itself is not installed by `setup.sh`; install it with your package manager (`brew install emacs`).

## Headless machines

On headless machines (e.g. Docker containers, servers), set `headless = true` to
disable GUI tools like kitty and emacs:

```sh
chezmoi edit-config   # add the following, then save:
```

```toml
[data]
headless = true
```

```sh
chezmoi apply
```

`headless` forces emacs and kitty off regardless of their individual flags; the
individual flags (`emacs`, `kitty`) still work independently on desktop machines.

## Daily usage

```sh
chezmoi apply              # apply changes after editing dot_* files
chezmoi update             # git pull + apply
chezmoi add ~/.foo         # start managing a new file
chezmoi re-add ~/.foo      # adopt changes made outside the repo (e.g. lazy-lock.json)
chezmoi diff               # preview what would change
chezmoi status             # show targets that differ from the source state
```

## Notes

- The repo is expected to live at `~/.dot-files` — `dot_shrc` sources `$HOME/.dot-files/.env`; shell helpers are installed by chezmoi to `~/.local/bin/`.
- `~/.gitconfig` is intentionally **not** managed because it carries machine-local proxy settings. The repo's git config is installed to `~/.config/git/`, which git reads in addition to `~/.gitconfig`.
- System packages (e.g. `zsh` on Linux) are not installed by `setup.sh`; install them with your package manager (`apt install zsh`, ...). Everything else is managed by mise.
- After Neovim plugin updates, `~/.config/NvChad/lazy-lock.json` may change — run `chezmoi re-add ~/.config/NvChad/lazy-lock.json` to sync it back into the repo.
- `windows/Microsoft.PowerShell_profile.ps1` is linked into `$PROFILE` by `windows/setup.ps`; it is not a chezmoi target.

## License

MIT — see [LICENSE](LICENSE).

# dotfiles

Personal dotfiles for macOS / Linux / Windows, managed with [chezmoi](https://www.chezmoi.io/).

The repository doubles as chezmoi's source directory. All managed files live under [`xdg-config/`](xdg-config/), which is declared as the chezmoi root in [`.chezmoiroot`](.chezmoiroot). Scripts, fonts, and this README live at the repo root and are not installed.

Tools and toolchains are installed by [mise](https://mise.jdx.dev/) from [`xdg-config/dot_config/mise/config.toml`](xdg-config/dot_config/mise/config.toml).

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
| `~/.zshrc`, `~/.shrc` | `xdg-config/dot_zshrc`, `xdg-config/dot_shrc` |
| `~/.vimrc`, `~/.ideavimrc` | `xdg-config/dot_vimrc`, `xdg-config/dot_ideavimrc` |
| `~/.spacemacs` | `xdg-config/dot_spacemacs` |
| `~/.config/git/*` | `xdg-config/dot_config/git/*` |
| `~/.config/tmux/*` | `xdg-config/dot_config/tmux/*` |
| `~/.config/NvChad/*` | `xdg-config/dot_config/NvChad/*` |
| `~/.config/kitty/*` | `xdg-config/dot_config/kitty/*` |
| `~/.config/mise/*` | `xdg-config/dot_config/mise/*` |

External git repos, cloned and updated by chezmoi on every apply (see [`.chezmoiexternal.toml`](xdg-config/.chezmoiexternal.toml)):

- [zplug](https://github.com/zplug/zplug) → `~/.config/zplug`
- [oh-my-tmux](https://github.com/gpakosz/.tmux) → `~/.config/oh-my-tmux`
- [Spacemacs](https://github.com/syl20bnr/spacemacs) → `~/.emacs.d`
- [limo-spacemacs-layers](https://github.com/limoiie/limo-spacemacs-layers) → `~/.emacs.d/private/layers`

## Daily usage

```sh
chezmoi apply              # apply changes after editing files in xdg-config/
chezmoi update             # git pull + apply
chezmoi add ~/.foo         # start managing a new file
chezmoi re-add ~/.foo      # adopt changes made outside the repo (e.g. lazy-lock.json)
chezmoi diff               # preview what would change
chezmoi status             # show targets that differ from the source state
```

## Notes

- The repo is expected to live at `~/.dot-files` — `xdg-config/dot_shrc` sources `$HOME/.dot-files/.env` and `$HOME/.dot-files/scripts/*`.
- `~/.gitconfig` is intentionally **not** managed because it carries machine-local proxy settings. The repo's git config is installed to `~/.config/git/`, which git reads in addition to `~/.gitconfig`.
- System packages (e.g. `emacs` on macOS, `zsh` on Linux) are not installed by `setup.sh`; install them with your package manager (`brew install emacs`, `apt install zsh`, ...). Everything else is managed by mise.
- After Neovim plugin updates, `~/.config/NvChad/lazy-lock.json` may change — run `chezmoi re-add ~/.config/NvChad/lazy-lock.json` to sync it back into the repo.
- `windows/Microsoft.PowerShell_profile.ps1` is linked into `$PROFILE` by `windows/setup.ps`; it is not a chezmoi target.

## License

MIT — see [LICENSE](LICENSE).

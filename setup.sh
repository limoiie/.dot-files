#!/usr/bin/env bash
set -euo pipefail

DOT_FILES_ROOT="${HOME}/.dot-files"
REPO_URL="${DOTFILES_REPO_URL:-https://github.com/limoiie/.dot-files.git}"

# Install mise (tool and toolchain manager)
if ! command -v mise >/dev/null 2>&1; then
    curl -fsSL https://mise.run | sh
fi

# Install chezmoi (dotfile manager)
if ! command -v chezmoi >/dev/null 2>&1; then
    sh -c "$(curl -fsLS get.chezmoi.io)"
fi

export PATH="${HOME}/.local/bin:${PATH}"

# Clone the dotfiles repo if it is not present yet
if [ ! -d "${DOT_FILES_ROOT}/.git" ]; then
    git clone "${REPO_URL}" "${DOT_FILES_ROOT}"
fi

# Point chezmoi's source directory at the repo
mkdir -p "${HOME}/.local/share"
ln -sfn "${DOT_FILES_ROOT}" "${HOME}/.local/share/chezmoi"

# Generate the chezmoi config (from xdg-config/.chezmoi.toml.tmpl) and apply
chezmoi init
chezmoi apply

# Install mise-managed tools and toolchains (config.toml is installed above)
mise install

cat <<'EOF'

Dotfiles applied. Next steps:
  >> chezmoi apply        # apply changes after editing files in xdg-config/
  >> chezmoi update       # pull the repo and re-apply
  >> chezmoi add ~/.foo   # start managing a new file
  >> mise install         # (re)install tools listed in mise/config.toml
EOF

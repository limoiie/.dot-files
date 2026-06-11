#!/usr/bin/env bash
set -euo pipefail

DOT_FILES_ROOT="${HOME}/.dot-files"
DOT_CONFIG_HOME="${DOT_FILES_ROOT}/xdg-config"
XDG_CONFIG_HOME="${XDG_CONFIG_HOME:-${HOME}/.config}"

if ! command -v mise >/dev/null 2>&1; then
    curl -fsSL https://mise.run | sh
fi

export PATH="${HOME}/.local/bin:${PATH}"

mkdir -p "${XDG_CONFIG_HOME}"
ln -sfn "${DOT_CONFIG_HOME}/mise" "${XDG_CONFIG_HOME}/mise"

mise install

cd "${DOT_FILES_ROOT}"
mise exec -- uv tool install --editable .

cat <<'EOF'

dofu is installed. Next steps:
  >> dofu help              # show help
  >> dofu list              # list available modules
  >> dofu equip <module>    # set up a module
EOF

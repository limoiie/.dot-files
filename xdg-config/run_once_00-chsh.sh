#!/bin/sh
# Ensure the login shell is zsh. No-op when zsh is already the shell.
set -eu

if command -v zsh >/dev/null 2>&1; then
    zsh_path="$(command -v zsh)"
    if [ -n "${SHELL:-}" ] && [ "$SHELL" != "$zsh_path" ]; then
        chsh -s "$zsh_path"
    fi
fi

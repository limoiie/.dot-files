#!/bin/sh

export DOT_FILES_ROOT=$HOME/.dotfiles

poetry run -C $DOT_FILES_ROOT python3 -m dofu "$@"

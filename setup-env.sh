#!/bin/bash

RAW_GITHUB=https://raw.githubusercontent.com
DOT_FILES_ROOT=~/.dot-files

download-dot-files() {
    set -e

    git clone https://github.com/limoiie/.dot-files.git ${DOT_FILES_ROOT}
}

install-useful-dist-tools() {
    set -e

    echo "Install dist packages..."
    apt-get update \
        && apt-get install -y \
                   build-essential \
                   curl \
                   gawk \
                   git \
                   zsh

    apt-get install -y neovim
    apt-get install -y emacs
}

install-useful-tools() {
    set -e

    echo "Install useful command-line tools..."
    curl -fsSL https://sh.rustup.rs | bash -s -- -y
    . ~/.cargo/env \
        && cargo install \
                 bat \
                 exa \
                 fd-find \
                 ripgrep

    git clone --depth 1 https://github.com/junegunn/fzf.git ~/.fzf && \
        ~/.fzf/install --yes

    curl -fsSL https://starship.rs/install.sh | sh -s -- --yes
    curl -fsSL ${RAW_GITHUB}/zplug/installer/master/installer.zsh | zsh -s
}

configure-tools-and-shell() {
    set -e

    echo "Configure tools and shell..."
    mkdir -p ~/.config

    config-git
    config-vim
    config-emacs

    config-zsh
    config-shell-theme
}

config-git() {
    set -e

    echo "Configure git..."
    backup-file ~/.git-commit-template
    backup-file ~/.gitconfig
    ln -s ${DOT_FILES_ROOT}/.git-commit-template ~/.git-commit-template
    ln -s ${DOT_FILES_ROOT}/.gitconfig ~/.gitconfig
}

config-vim() {
    set -e

    echo "Configure vim..."
    echo "  - Download NvChad..."
    git clone https://github.com/NvChad/NvChad ~/.config/nvim
    echo "  - Download plug.vim..."
    curl -fsSLo ~/.local/share/nvim/site/autoload/plug.vim --create-dirs \
         ${RAW_GITHUB}/junegunn/vim-plug/master/plug.vim

    echo "  - Integrate .common-vimrc into .vimrc..."
    append-line 1 "source ${DOT_FILES_ROOT}/.common-vimrc" ~/.vimrc ".common-vimrc"

    echo "  - Adopt init.lua..."
    mkdir -p ~/.config/nvim
    backup-file ~/.config/nvim/init.lua
    ln -s ${DOT_FILES_ROOT}/.config/nvim/init.lua ~/.config/nvim/init.lua
}

config-emacs() {
    set -e

    echo "Configure emacs..."
    echo "  - Download spacemacs..."
    git clone https://github.com/syl20bnr/spacemacs.git ~/.emacs.d
    echo "  - Download limo spacemacs layers..."
    git clone https://github.com/limoiie/limo-spacemacs-layers.git \
        ~/.emacs.d/private/layers

    echo "  - Adopt .spacemacs..."
    backup-file ~/.spacemacs
    cp ${DOT_FILES_ROOT}/.spacemacs ~/.spacemacs
}

config-zsh() {
    set -e

    echo "Configure zsh..."
    echo "  - Integrate common-used shell config into .zshrc..."
    append-line 1 ". ${DOT_FILES_ROOT}/.common-shrc"  ~/.zshrc ".common-shrc"
    append-line 1 ". ${DOT_FILES_ROOT}/.common-zshrc" ~/.zshrc ".common-zshrc"
}

config-shell-theme() {
    set -e

    echo "Config shell theme"
    echo "  - Choose starship"
    backup-file ~/.config/starship.toml
    ln -s ${DOT_FILES_ROOT}/.config/starship.toml ~/.config/starship.toml
}

backup-file() {
    [ -f "$1" ] && mv "$1" "$1.bk"
}

append-line() {
    set -e

    local update line file pat lno
    update="$1"
    line="$2"
    file="$3"
    pat="${4:-}"
    lno=""

    echo "Update $file:"
    echo "  - $line"
    if [ -f "$file" ]; then
        if [ $# -lt 4 ]; then
            lno=$(\grep -nF "$line" "$file" | sed 's/:.*//' | tr '\n' ' ')
        else
            lno=$(\grep -nF "$pat" "$file" | sed 's/:.*//' | tr '\n' ' ')
        fi
    fi
    if [ -n "$lno" ]; then
        echo "    - Already exists: line #$lno"
    else
        if [ $update -eq 1 ]; then
            [ -f "$file" ] && echo >> "$file"
            echo "$line" >> "$file"
            echo "    + Added"
        else
            echo "    ~ Skipped"
        fi
    fi
    echo
    set +e
}

install-useful-dist-tools
install-useful-tools
download-dot-files
configure-tools-and-shell

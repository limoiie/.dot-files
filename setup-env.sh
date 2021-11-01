#!/bin/bash

RAW_GIT=https://raw.githubusercontent.com
DOT_FILES_ROOT=~/.dot-files

download-dot-files() {
    git clone https://github.com/limoiie/.dot-files.git ${DOT_FILES_ROOT}
}

install-useful-dist-tools() {
    sudo apt-get update \
        && apt-get install -y \
                   build-essential \
                   curl \
                   gawk \
                   git \
                   zsh

    sudo apt-get udpate \
        && apt-get install -y neovim

    sudo apt-get update \
        && apt-get install -y emacs
}

install-useful-tools() {
    curl -fsSL https://sh.rustup.rs | bash -s -- -y
    . ~/.cargo/env \
        && cargo install \
                 bat \
                 exa \
                 fd-find \
                 ripgrep

    git clone --depth 1 https://github.com/junegunn/fzf.git ~/.fzf && \
        ~/.fzf/install

    curl -fsSL https://starship.rs/install.sh | sh -s -- --yes
    curl -fsSL ${RAW_GIT}/zplug/installer/master/installer.zsh | zsh -s
}

configure-tools-and-shell() {
    mkdir -p ~/.config

    config-git
    config-vim
    config-emacs

    config-zsh
    config-shell-theme
}

config-git() {
    ln -s ${DOT_FILES_ROOT}/.git-commit-template ~/.git-commit-template
    ln -s ${DOT_FILES_ROOT}/.gitconfig ~/.gitconfig
}

config-vim() {
    git clone https://github.com/NvChad/NvChad ~/.config/nvim
    curl -fsSLo ~/.local/share/nvim/site/autoload/plug.vim --create-dirs \
         ${RAW_GIT}/junegunn/vim-plug/master/plug.vim

    if [ -z $(grep 'common-vimrc' ~/.vimrc) ]; then
        echo '\nsource ${DOT_FILES_ROOT}/.common-vimrc\n'
    fi
    mkdir -p ~/.config/nvim
    ln -s ${DOT_FILES_ROOT}/.config/nvim/init.lua ~/.config/nvim/init.lua
}

config-emacs() {
    git clone https://github.com/sy120bnr/spacemcs ~/.emacs.d
    git clone https://github.com/limoiie/limo-spacemacs-layers.git \
        ~/.emacs.d/private/layers
    cp ${DOT_FILES_ROOT}/.spacemacs ~/.spacemacs
}

config-zsh() {
    if [ -z $(grep '.common-shrc' ~/.zshrc) ]; then
        echo "\n. ${DOT_FILES_ROOT}/.common-shrc\n" >> ~/.zshrc
    fi
    if [ -z $(grep '.common-zshrc' ~/.zshrc) ]; then
        echo "\n. ${DOT_FILES_ROOT}/.common-zshrc\n" >> ~/.zshrc
    fi
}

config-shell-theme() {
    ln -s ${DOT_FILES_ROOT}/.config/starship.toml ~/.config/starship.toml
}

install-useful-dist-tools
install-useful-tools
download-dot-files
configre-tools-and-shell

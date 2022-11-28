#!/bin/bash

install-useful-dist-tools() {
    set -e

    echo "Install dist packages..."
    apt-get update -o Acquire::http::proxy=false \
        && apt-get install -o Acquire::http::proxy=false -y \
                   build-essential \
                   curl \
                   gawk \
                   git \
                   zsh \
        || exit -1
    apt-get install -o Acquire::http::proxy=false -y software-properties-common \
        && add-apt-repository -y ppa:neovim-ppa/stable \
        && add-apt-repository -y ppa:ubuntu-elisp/ppa \
        && apt-get update -o Acquire::http::proxy=false \
        && apt-get install -o Acquire::http::proxy=false -y \
                   neovim \
                   emacs-snapshot \
        || exit -1

    set +e
}

install-useful-modern-tools() {
    set -e

    echo "Install useful modern command-line tools..."
    run-remote-script https://sh.rustup.rs sh
    . ~/.cargo/env \
        && cargo install \
                 bat \
                 exa \
                 fd-find \
                 procs \
                 ripgrep \
                 sd \
        || exit -1

    git clone --depth 1 https://github.com/junegunn/fzf.git ~/.fzf \
        && ~/.fzf/install --all \
        || exit -1

    set +e
}

run-remote-script() {
    set -eu
    
    local url shcmd tmp
    url=$1
    shcmd=$2

    tmp=$(mktemp '/tmp/setup-env-run-remote-XXXX')
    curl -L $url -o $tmp \
        && $shcmd $tmp -y ${@:3} \
        || (rm -rf $tmp && exit -1)
    rm -f $tmp

    set +eu
}

install-useful-dist-tools
install-useful-modern-tools

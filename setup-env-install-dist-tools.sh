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

install-useful-dist-tools

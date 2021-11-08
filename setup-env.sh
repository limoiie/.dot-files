#!/bin/bash

RAW_GITHUB=https://raw.githubusercontent.com
DOT_FILES_ROOT=~/.dot-files

ACTION=${1:-1111}

download-dot-files() {
    set -e

    git clone https://github.com/limoiie/.dot-files.git ${DOT_FILES_ROOT}

    set +e
}

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

install-useful-other-tools() {
    set -e

    echo "Install useful command-line tools..."
    run_remote_script https://sh.rustup.rs sh
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

configure-tools-and-shell() {
    set -e

    echo "Configure tools and shell..."
    mkdir -p ~/.config

    config-git
    config-vim
    config-emacs

    config-zsh
    config-shell-theme

    echo "Congratulations! All done~"

    set +e
}

config-git() {
    set -e

    echo "Configure git..."
    backup-file ~/.git-commit-template
    backup-file ~/.gitconfig
    echo "  - Link .git-commit-template and .gitconfig"
    ln -s ${DOT_FILES_ROOT}/.git-commit-template ~/.git-commit-template
    ln -s ${DOT_FILES_ROOT}/.gitconfig ~/.gitconfig

    set +e
}

config-vim() {
    set -e

    echo "Configure vim..."
    echo "  - Download NvChad..."
    git clone https://github.com/NvChad/NvChad ~/.config/nvim
    echo "  - Download plug.vim..."
    curl -Lo ~/.local/share/nvim/site/autoload/plug.vim --create-dirs \
         ${RAW_GITHUB}/junegunn/vim-plug/master/plug.vim

    echo "  - Integrate .common-vimrc into .vimrc..."
    append-line 1 "source ${DOT_FILES_ROOT}/.common-vimrc" ~/.vimrc ".common-vimrc"

    echo "  - Config nvim customized configuration..."
    mkdir -p ~/.config/nvim/lua/custom
    backup-file ~/.config/nvim/lua/custom/init.lua
    backup-file ~/.config/nvim/lua/custom/chadrc.lua
    echo "  - Link customized init.lua and chadrc.lua"
    ln -s ${DOT_FILES_ROOT}/.config/nvim/lua/custom/init.lua ~/.config/nvim/lua/custom/init.lua
    ln -s ${DOT_FILES_ROOT}/.config/nvim/lua/custom/chadrc.lua ~/.config/nvim/lua/custom/chadrc.lua

    set +e
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

    set +e
}

config-zsh() {
    set -e

    echo "Configure zsh..."
    echo "  - Download zplug..."
    run_remote_script ${RAW_GITHUB}/zplug/installer/master/installer.zsh zsh
    echo "  - Integrate common-used shell config into .zshrc..."
    append-line 1 ". ${DOT_FILES_ROOT}/.common-shrc"  ~/.zshrc ".common-shrc"
    append-line 1 ". ${DOT_FILES_ROOT}/.common-zshrc" ~/.zshrc ".common-zshrc"

    set +e
}

config-shell-theme() {
    set -e

    echo "Config shell theme"
    echo "  - Download starship"
    run_remote_script https://starship.rs/install.sh sh
    echo "  - Integrate starship init .zshrc..."
    append-line 1 'eval "$(starship init zsh)"' ~/.zshrc "starship init zsh"
    backup-file ~/.config/starship.toml
    echo "  - Link starship.toml"
    ln -s ${DOT_FILES_ROOT}/.config/starship.toml ~/.config/starship.toml

    set +e
}

run_remote_script() {
    set -eu
    
    local script_url, sh_cmd, tmp
    script_url=$1
    sh_cmd=$2

    tmp=$(mktemp '/tmp/setup-env-run-remote-xxxx')
    curl -L ${script_url} -o ${tmp} \
        && ${sh_cmd} ${tmp} -y ${@:2} \
        || (rm -rf ${tmp} && exit -1)
    rm -f ${tmp}

    set +eu
}

backup-file() {
    if [ -f "${1}" ]; then
        echo "  - Backup existing ${1}"
        mv "${1}" "${1}.bk"
    fi
}

append-line() {
    set -e

    local update line file pat lno
    update="$1"
    line="$2"
    file="$3"
    pat="${4:-}"
    lno=""

    echo "  - Update $file:"
    echo "    - $line"
    if [ -f "$file" ]; then
        if [ $# -lt 4 ]; then
            lno=$(\grep -nF "$line" "$file" | sed 's/:.*//' | tr '\n' ' ')
        else
            lno=$(\grep -nF "$pat" "$file" | sed 's/:.*//' | tr '\n' ' ')
        fi
    fi
    if [ -n "$lno" ]; then
        echo "      - Already exists: line #$lno"
    else
        if [ $update -eq 1 ]; then
            [ -f "$file" ] && echo >> "$file"
            echo "$line" >> "$file"
            echo "      + Added"
        else
            echo "      ~ Skipped"
        fi
    fi
    set +e
}

if ! [[ ${ACTION} =~ [01]{4} ]]; then
    echo "Error: Unknown action: $1, should be in `[01]{4}`."; exit -1
fi

if [[ ${ACTION} =~ 1... ]]; then install-useful-dist-tools; fi
if [[ ${ACTION} =~ .1.. ]]; then install-useful-other-tools; fi
if [[ ${ACTION} =~ ..1. ]]; then download-dot-files; fi
if [[ ${ACTION} =~ ...1 ]]; then configure-tools-and-shell; fi


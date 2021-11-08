#!/bin/bash

DOT_FILES_ROOT=~/.dot-files

ACTION=${1:-init}  # init, update, overwrite

download-dot-files() {
    set -e

    git-clone-safely https://github.com/limoiie/.dot-files.git ${DOT_FILES_ROOT}

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
    ln-safely -s ${DOT_FILES_ROOT}/.git-commit-template ~/.git-commit-template
    ln-safely -s ${DOT_FILES_ROOT}/.gitconfig ~/.gitconfig

    set +e
}

config-vim() {
    set -e

    echo "Configure vim..."
    echo "  - Download NvChad..."
    git-clone-safely https://github.com/NvChad/NvChad ~/.config/nvim
    echo "  - Download plug.vim..."
    curl-safely -L --create-dirs https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim \
         -o ~/.local/share/nvim/site/autoload/plug.vim 

    echo "  - Integrate .common-vimrc into .vimrc..."
    append-line 1 "source ${DOT_FILES_ROOT}/.common-vimrc" ~/.vimrc ".common-vimrc"

    echo "  - Config nvim customized configuration..."
    mkdir -p ~/.config/nvim/lua/custom
    ln-safely -s ${DOT_FILES_ROOT}/.config/nvim/lua/custom/init.lua ~/.config/nvim/lua/custom/init.lua
    ln-safely -s ${DOT_FILES_ROOT}/.config/nvim/lua/custom/chadrc.lua ~/.config/nvim/lua/custom/chadrc.lua
    ln-safely -s ${DOT_FILES_ROOT}/.config/nvim/lua/custom/plugins ~/.config/nvim/lua/custom/plugins

    set +e
}

config-emacs() {
    set -e

    echo "Configure emacs..."
    echo "  - Download spacemacs"
    git-clone-safely https://github.com/syl20bnr/spacemacs.git ~/.emacs.d
    echo "  - Download limo spacemacs layers..."
    git-clone-safely https://github.com/limoiie/limo-spacemacs-layers.git \
        ~/.emacs.d/private/layers

    echo "  - Adopt .spacemacs..."
    cp-safely ${DOT_FILES_ROOT}/.spacemacs ~/.spacemacs

    set +e
}

config-zsh() {
    set -e

    echo "Configure zsh..."
    echo "  - Download zplug..."
    run-remote-script https://raw.githubusercontent.com/zplug/installer/master/installer.zsh zsh
    echo "  - Integrate common-used shell config into .zshrc..."
    append-line 1 ". ${DOT_FILES_ROOT}/.common-shrc"  ~/.zshrc ".common-shrc"
    append-line 1 ". ${DOT_FILES_ROOT}/.common-zshrc" ~/.zshrc ".common-zshrc"

    set +e
}

config-shell-theme() {
    set -e

    echo "Config shell theme"
    echo "  - Download starship"
    run-remote-script https://starship.rs/install.sh sh
    echo "  - Integrate starship init .zshrc..."
    append-line 1 'eval "$(starship init zsh)"' ~/.zshrc "starship init zsh"
    ln-safely -s ${DOT_FILES_ROOT}/.config/starship.toml ~/.config/starship.toml

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

ln-safely() {
    local src tgt
    tgt=${@: -1}
    src=${@: -2}
    
    case $ACTION in
      init | update)
        if [ -L $tgt ]; then
            remove-file $tgt
            echo "  - Link $src -> $tgt"
            ln $@
        else
            backup-file $tgt
            echo "  - Link $src -> $tgt"
            ln $@
        fi
        ;;

      overwrite)
        remove-file $tgt
        echo "  - Link $src -> $tgt"
        ln $@
        ;;
    esac
}

cp-safely() {
    local src tgt
    tgt=${@: -1}
    src=${@: -2}

    case $ACTION in
      init | update)
        if [ cmp --silent $tgt $src ]; then
            echo "  - Skip copying identity file" 
        else
            backup-file $tgt
            echo "  - Copy $src -> $tgt"
            cp $@
        fi
        ;;

      overwrite)
        remove-file $tgt
        echo "  - Copy $src -> $tgt"
        cp $@
        ;;
    esac
}

git-clone-safely() {
    local src tgt action
    tgt=${@: -1}
    src=${@: -2}

    case $ACTION in
      init | update)
        if [ -d "$tgt" ] && [ -d "$tgt/.git" ]; then
            echo "  - Update $tgt..."
            (cd "$file" && git pull)
        else
            backup-file $tgt
            echo "  - Clone $src -> $tgt..."
            git clone $@
        fi
        ;;

      overwrite)
        remove-file $tgt
        echo "  - Clone $src -> $tgt..."
        git clone $@
        ;;
    esac
}

curl-safely() {
    local src tgt
    tgt=${@: -1}
    src=${@: -3}

    case $ACTION in
      init)
        backup-file $tgt
        echo "  - Download -> $tgt..."
        curl $@
        ;;

      update | overwrite)
        remove-file $tgt
        echo "  - Download -> $tgt..."
        curl $@
        ;;
    esac
}

backup-file() {
    local file bkfile
    file="$1"
    bkfile="$file.bk"
    if [ -e "$file" ]; then
        echo "  - Backup existing $file"
        while [ -e $bkfile ]; do
            bkfile="$bkfile.bk"
        done
        mv "$file" "$bkfile"
    fi
}

remove-file() {
    local file
    file="$1"
    echo "  - Remove existing $file"
    rm -rf $file
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

download-dot-files
configure-tools-and-shell


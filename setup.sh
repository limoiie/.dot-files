#!/bin/bash

DOT_FILES_ROOT=~/.dot-files
DOT_CONFIG_HOME=${DOT_FILES_ROOT}/.config
XDG_CONFIG_HOME=~/.config

ACTION=${1:-init}  # init, update, overwrite
PACKAGES=${@:2}

install-basic-tools() {
    set -e

    echo "Install basic tools..."
    apt install -y git curl

    set +e
}

download-dot-files() {
    set -e

    echo "Download/Update dot-files..."
    git-clone-safely https://github.com/limoiie/.dot-files.git ${DOT_FILES_ROOT}

    set +e
}

configure-tools-and-shell() {
    set -e

    echo "Configure tools and shell: ${PACKAGES}..."
    mkdir -p ${XDG_CONFIG_HOME}

    is-enabled git && config-git
    is-enabled cargo && config-cargo
    is-enabled go && config-go

    is-enabled py && config-py

    is-enabled vim && config-vim
    is-enabled emacs && config-emacs

    is-enabled zsh && config-zsh
    is-enabled fzf && config-fzf
    is-enabled shell-theme && config-shell-theme

    echo "Congratulations! All done~"

    set +e
}

config-git() {
    set -e

    echo "Configure git..."
    ln-safely -s ${DOT_CONFIG_HOME}/git ${XDG_CONFIG_HOME}/git

    set +e
}

config-cargo() {
    set -e

    echo "Install useful modern command-line tools..."
    [ -x "$(which cargo)" ] || \
        curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
    . $HOME/.cargo/env \
        && cargo install \
                 bat \
                 exa \
                 fd-find \
                 procs \
                 ripgrep \
                 sd

    set +e
}

config-go() {
    set -e

    echo "Install useful modern command-line tools written in go..."
    [ -x "$(which go)" ] || \
        (echo "Please install go at first!"; exit -1)
    go install \
        github.com/jesseduffield/lazydocker@latest \
        github.com/jesseduffield/lazygit@latest

    set +e
}

config-py() {
    set -e

    pip install poetry

    set +e
}

config-vim() {
    set -e

    echo "Download bob-nvim..."
    cargo install bob-nvim

    echo "Download latest neovim ..."
    bob use latest

    echo "Configure vim..."
    echo "  - Integrate .common-vimrc into .vimrc..."
    mkdir -p ${XDG_CONFIG_HOME}/vim
    mv-safely ~/.vimrc ${XDG_CONFIG_HOME}/vim/vimrc
    mv-safely ~/.viminfo ${XDG_CONFIG_HOME}/vim/viminfo
    append-line 1 "source ${DOT_FILES_ROOT}/.common-vimrc" ${XDG_CONFIG_HOME}/vim/vimrc ".common-vimrc"

    echo "Configure NvChad..."
    echo "  - Download NvChad..."
    git-clone-safely https://github.com/NvChad/NvChad ${XDG_CONFIG_HOME}/NvChad
    echo "  - Customize NvChad..."
    ln-safely -s ${DOT_CONFIG_HOME}/NvChad/lua/custom ${XDG_CONFIG_HOME}/NvChad/lua/custom

    set +e
}

config-emacs() {
    set -e

    echo "Install emacs..."
    [ -x "$(which emacs)" ] || \
        sudo snap install emacs --classic

    echo "Configure emacs..."
    echo "  - Download spacemacs"
    git-clone-safely https://github.com/syl20bnr/spacemacs.git ~/.emacs.d
    echo "  - Download limo spacemacs layers..."
    git-clone-safely https://github.com/limoiie/limo-spacemacs-layers.git \
        ~/.emacs.d/private/layers

    echo "  - See also ${DOT_FILES_ROOT}/.spacemacs..."

    set +e
}

config-zsh() {
    set -e

    echo "Configure zsh..."
    if [ -e ~/.zplug ]; then
        echo "  - Migrate existing .zplug to ${XDG_CONFIG_HOME}/zplug..."
        mv-safely ~/.zplug ${XDG_CONFIG_HOME}/zplug
    fi
    echo "  - Download zplug to ${XDG_CONFIG_HOME}/zplug..."
    git-clone-safely https://github.com/zplug/zplug.git ${XDG_CONFIG_HOME}/zplug
    echo "  - Integrate common-used shell config into .zshrc..."
    append-line 1 ". ${DOT_FILES_ROOT}/.common-shrc"  ~/.zshrc ".common-shrc"
    append-line 1 ". ${DOT_FILES_ROOT}/.common-zshrc" ~/.zshrc ".common-zshrc"

    set +e
}

config-fzf() {
    set -e

    echo "Configure fzf..."
    git-clone-safely --depth 1 https://github.com/junegunn/fzf.git ${XDG_CONFIG_HOME}/fzf \
        && ${XDG_CONFIG_HOME}/fzf/install --all \
        || exit -1
    
    echo "  - Move fzf scripts to ${XDG_CONFIG_HOME}/"
    mv-safely $HOME/.fzf.bash ${XDG_CONFIG_HOME}/fzf.bash
    mv-safely $HOME/.fzf.zsh ${XDG_CONFIG_HOME}/fzf.zsh

    sed -i -- 's/^.*\-f ~\/.fzf.bash.*$/[ -f ~\/.config\/fzf.bash ] \&\& source ~\/.config\/fzf.bash/' $HOME/.bashrc
    sed -i -- 's/^.*\-f ~\/.fzf.zsh.*$/[ -f ~\/.config\/fzf.zsh ] \&\& source ~\/.config\/fzf.zsh/' $HOME/.zshrc

    set +e
}

config-shell-theme() {
    set -e

    echo "Config shell theme"
    echo "  - Download starship"
    [ -x "$(which starship)" ] || \
      run-remote-script https://starship.rs/install.sh sh
    echo "  - Integrate starship init .zshrc..."
    append-line 1 "export STARSHIP_CONFIG=${DOT_CONFIG_HOME}/starship.toml" ~/.zshrc \
      "export STARSHIP_CONFIG"
    append-line 1 'eval "$(starship init zsh)"' ~/.zshrc "starship init zsh"

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
    src=${@: -2:1}
    
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
    src=${@: -2:1}

    if [ ! -e $src ]; then
        echo "  - Skip copying non-existing file"
        return 0
    fi

    case $ACTION in
      init | update)
        if [ cmp --silent $tgt $src ]; then
            echo "  - Skip copying identity file" 
            return 0
        fi
        backup-file $tgt
        ;;

      overwrite)
        remove-file $tgt
        ;;
    esac
    echo "  - Copy $src -> $tgt"
    cp $@
}

mv-safely() {
    local src tgt
    tgt="${@: -1}"
    src="${@: -2:1}"

    if [ ! -e $src ]; then
        echo "  - Skip moving non-existing file"
        return 0
    fi

    case $ACTION in
      init | update)
        if [ cmp --slient $tgt $src ]; then
            echo "  - Skip moving identity file"
            return 0
        fi
        backup-file $tgt
        ;;
      overwrite)
        remove-file $tgt
        ;;
    esac
    echo "  - Move $src -> $tgt"
    mv $@
}

git-clone-safely() {
    local src tgt action
    tgt=${@: -1}
    src=${@: -2:1}

    case $ACTION in
      init | update)
        if [ -d "$tgt" ] && [ -d "$tgt/.git" ]; then
            echo "  - Update $src -> $tgt..."
            (cd "$tgt" && git pull)
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
    src=${@: -3:1}

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

is-enabled() {
    local package
    package=$1
    [ "${PACKAGES}" == all ] && return 0
    contains $package ${PACKAGES} && return 0
    return 1
}

contains() {
    local target elem
    target=$1
    shift
    for elem  # implicitly iterate remain args
    do 
        [ "$elem" == "$target" ] && return 0
    done
    return 1
}

install-basic-tools
download-dot-files
configure-tools-and-shell


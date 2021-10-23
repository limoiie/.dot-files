# If you come from bash you might have to change your $PATH.
# export PATH=$HOME/bin:/usr/local/bin:$PATH
# Path to your oh-my-zsh installation.
export ZSH=$HOME/.oh-my-zsh

export PATH=/home/limo/.local/bin:/usr/local/cuda-11.4/bin:$PATH
export PATH=/opt/cmake-3.15.0-rc2-Linux-x86_64/bin:$PATH

export LD_LIBRARY_PATH=/usr/local/cuda-11.4/lib64:$LD_LIBRARY_PATH
export PYTHONPATH=/home/limo/Projects/research/asm2vec_rebuild:$PYTHONPATH
export MANPAGER="sh -c 'col -bx | bat -l man -p'"

# fzf options
export FZF_DEFAULT_OPTS='--height 40% --layout=reverse --border --bind="ctrl-k:kill-line,ctrl-v:page-down,alt-v:page-up,alt-n:preview-page-down,alt-p:preview-page-up"'
export FZF_COMPLETION_TRIGGER='..'

export LC_CTYPE=en_US.UTF-8
export LC_ALL=en_US.UTF-8

fpath=("$HOME/.zfunctions" $fpath)

# Set name of the theme to load. Optionally, if you set this to "random"
# it'll load a random theme each time that oh-my-zsh is loaded.
# See https://github.com/robbyrussell/oh-my-zsh/wiki/Themes
# ZSH_THEME="robbyrussell"
# ZSH_THEME="agnoster"
# ZSH_THEME="agnoster-cust"
# ZSH_THEME="miloshadzic"
# ZSH_THEME="dracula"

# Uncomment the following line to use case-sensitive completion.
# CASE_SENSITIVE="true"

# Uncomment the following line to use hyphen-insensitive completion. Case
# sensitive completion must be off. _ and - will be interchangeable.
# HYPHEN_INSENSITIVE="true"

# Uncomment the following line to disable bi-weekly auto-update checks.
# DISABLE_AUTO_UPDATE="true"

# Uncomment the following line to change how often to auto-update (in days).
# export UPDATE_ZSH_DAYS=13

# Uncomment the following line to disable colors in ls.
# DISABLE_LS_COLORS="true"

# Uncomment the following line to disable auto-setting terminal title.
# DISABLE_AUTO_TITLE="true"

# Uncomment the following line to enable command auto-correction.
# ENABLE_CORRECTION="true"

# Uncomment the following line to display red dots whilst waiting for completion.
# COMPLETION_WAITING_DOTS="true"

# Uncomment the following line if you want to disable marking untracked files
# under VCS as dirty. This makes repository status check for large repositories
# much, much faster.
# DISABLE_UNTRACKED_FILES_DIRTY="true"

# Uncomment the following line if you want to change the command execution time
# stamp shown in the history command output.
# The optional three formats: "mm/dd/yyyy"|"dd.mm.yyyy"|"yyyy-mm-dd"
# HIST_STAMPS="mm/dd/yyyy"

# Would you like to use another custom folder than $ZSH/custom?
# ZSH_CUSTOM=/path/to/new-custom-folder

# Which plugins would you like to load? (plugins can be found in ~/.oh-my-zsh/plugins/*)
# Custom plugins may be added to ~/.oh-my-zsh/custom/plugins/
# Example format: plugins=(rails git textmate ruby lighthouse)
# Add wisely, as too many plugins slow down shell startup.
plugins=(z git wd cargo rust pip zsh-syntax-highlighting zsh-autosuggestions)

source $ZSH/oh-my-zsh.sh

# User configuration

# export MANPATH="/usr/local/man:$MANPATH"

# You may need to manually set your language environment
# export LANG=en_US.UTF-8

# Preferred editor for local and remote sessions
# if [[ -n $SSH_CONNECTION ]]; then
#   export EDITOR='vim'
# else
#   export EDITOR='mvim'
# fi

# Compilation flags
# export ARCHFLAGS="-arch x86_64"

# ssh
# export SSH_KEY_PATH="~/.ssh/rsa_id"

# Set personal aliases, overriding those provided by oh-my-zsh libs,
# plugins, and themes. Aliases can be placed here, though oh-my-zsh
# users are encouraged to define aliases within the ZSH_CUSTOM folder.
# For a full list of active aliases, run `alias`.
#
# Example aliases
# alias zshconfig="mate ~/.zshrc"
# alias ohmyzsh="mate ~/.oh-my-zsh"
alias ls="exa"
alias la="ls -al"
alias e="emacs"
alias et="emacs -nw"
alias en="emacs -nw"
alias ec="emacsclient -a '' -c"
alias v="nvim"
alias vi="nvim"

# For fg jobs
alias j1=%1
alias j2=%2
alias j3=%3
alias j4=%4
alias j5=%5

alias confzsh="emacs ~/.zshrc"
alias confemacs="emacs ~/.emacs.d/init.el"

# nvm configuration
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion

# >>> conda initialize >>>
# !! Contents within this block are managed by 'conda init' !!
__conda_setup="$('/opt/anaconda3/bin/conda' 'shell.zsh' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
    eval "$__conda_setup"
else
    if [ -f "/opt/anaconda3/etc/profile.d/conda.sh" ]; then
        . "/opt/anaconda3/etc/profile.d/conda.sh"
    else
        export PATH="/opt/anaconda3/bin:$PATH"
    fi
fi
unset __conda_setup
# <<< conda initialize <<<
# conda activate /home/limo/.conda/envs/science_env/

# opam configuration
test -r /home/limo/.opam/opam-init/init.zsh && . /home/limo/.opam/opam-init/init.zsh > /dev/null 2> /dev/null || true

[ -f "/home/limo/.ghcup/env" ] && source "/home/limo/.ghcup/env" # ghcup-env

# >>> customized commands >>>
eval "$(starship init zsh)"

# enable fzf completioin and key-bindings
source /usr/share/doc/fzf/examples/completion.zsh
source /usr/share/doc/fzf/examples/key-bindings.zsh

# disable proxy
function proxy_off() {
    unset http_proxy
    unset https_proxy
    unset ftp_proxy
    unset rsync_proxy
    echo -e "Proxy is disabled"
}

# enable proxy
function proxy_on() {
    export no_proxy="localhost,127.0.0.1,localaddress,.localdomain.com"
    export http_proxy="http://127.0.0.1:7890"
    export https_proxy=$http_proxy
    export ftp_proxy=$http_proxy
    export rsync_proxy=$http_proxy
    echo -e "Proxy is enabled on $http_proxy!"
}

function run_clash() {
    screen -S clash -dm ~/Downloads/clash-linux-amd64-v1.3.0
}

# remove all the emacs swap files under current folder
function clean_emacs_cache() {
    rm .*~
}

# Boost z with fzf
function zf() {
    dir=$(z -l | tac | fzf | awk '{ $1="" }1' | sed 's/^ *//')
    if [[ -d "$dir" ]]; then
       cd $dir
    fi
}

# Call fzf with bat as preview
function fp() {
    preview="bat --color=always --style=numbers --line-range=:500 {}"
    fzf $@ --preview $preview
}

# Beautified git-diff boosted with bat and fzf
function gdf() {
    # {-1} stands for the selected file
    preview="git diff $@ --color=always -- {-1}"
    git diff $@ --name-only | fzf -m --height=100% --preview $preview
}

# Boost tail with bat
function bail() {
    tail $@ | bat --paging=never -l log
}

# Boost rg with fzf
function rgf() {
    INITIAL_QUERY="" RG_PREFIX="rg --column --line-number --no-heading --color=always --smart-case $@" \
                 FZF_DEFAULT_COMMAND="$RG_PREFIX '$INITIAL_QUERY'" \
                 fzf --bind "change:reload:$RG_PREFIX {q} || true" \
                 --ansi --query "$INITIAL_QUERY" \
                 --height=50% --layout=reverse
}
# <<< customized commands <<<

#!/bin/sh

COMMON_RC_URL=https://raw.githubusercontent.com/limoiie/.dot-files/master/.commonrc
STARSHIP_CONFIG_URL=https://raw.githubusercontent.com/limoiie/.dot-files/master/.config/starship.toml
VIM_CONFIG_URL=https://raw.githubusercontent.com/limoiie/.dot-files/master/.config/nvim/init.lua
VIM_RC_URL=https://raw.githubusercontent.com/limoiie/.dot-files/master/.config/nvim/init.lua

# Replace the text wrapped by OPEN_TAG and CLOSE_TAG in OUT_FILE with the
# text wrapped by these tags in IN_FILE.
# If the tags are missing in OUT_FILE, append them at the end of OUT_FILE.
# If the tags are missing in IN_FILE, wrap the whole file with the tags.
update_area() {
  OPEN_TAG=$1
  CLOSE_TAG=$2
  IN_FILE=$3
  OUT_FILE=$4

  ! [ -f "$OUT_FILE" ] && echo > "$OUT_FILE"

  TMP_IN_FILE=$(mktemp /tmp/tmpin.XXXX)
  cat "$IN_FILE" > $TMP_IN_FILE

  # out: append tags at the end of the file if no tags
  if [ -z "$(sed -e "/^$OPEN_TAG/,/^$CLOSE_TAG/!d" "$OUT_FILE")" ]; then
    sed -i -e "\$a$OPEN_TAG\n$CLOSE_TAG" "$OUT_FILE"
  fi

  # in: wrap the whole file with tags if no tags
  if [ -z "$(sed -e "/^$OPEN_TAG/,/^$CLOSE_TAG/!d" $TMP_IN_FILE)" ]; then
    sed -i -e "1s/^/$OPEN_TAG\n/" -e "\$a$CLOSE_TAG" $TMP_IN_FILE
  fi

  # in: only keep the text wrapped by the tags
  sed -i -e "/^$OPEN_TAG/,/^$CLOSE_TAG/!d" $TMP_IN_FILE

  # out: replace the text wrapped by tags of out with the text of in
  sed -i "$OUT_FILE" \
    -e "/^$OPEN_TAG/,/^$CLOSE_TAG/!b" \
    -e "/^$CLOSE_TAG/!d;r $TMP_IN_FILE" \
    -e 'd'

  rm $TMP_IN_FILE
}

adjust_zshrc() {
  # enable useful plugins by default
  cat <<EOT >> "$HOME/.zshrc"
# >>> zplug configure >>>
source "$HOME/.zplug/init.zsh"
zplug "plugins/z", from:oh-my-zsh
zplug "plugins/git", from:oh-my-zsh
zplug "zsh-users/zsh-syntax-highlighting"
zplug "zsh-users/zsh-autosuggestions"

# zplug check returns true if all packages are installed
# Therefore, when it returns false, run zplug install
if ! zplug check; then
    zplug install
fi

# source plugins and add commands to the PATH
zplug load
# <<< zplug configure <<<
EOT
  zsh -c "source /root/.zshrc"
}

update_xshrc() {
  OPEN_TAG="# >>> shared customization >>>"
  CLOSE_TAG="# <<< shared customization <<<"

  TMP_RC=$(mktemp /tmp/tmp-rc.XXXX)

  curl $COMMON_RC_URL -fsSL > $TMP_RC || exit -1

  update_area "$OPEN_TAG" "$CLOSE_TAG" $TMP_RC "$HOME/.bashrc" && \
  update_area "$OPEN_TAG" "$CLOSE_TAG" $TMP_RC "$HOME/.zshrc"

  adjust_zshrc

  rm $TMP_RC
}

update_starship_config() {
  mkdir -p "$HOME/.config" &&
    curl $STARSHIP_CONFIG_URL -fsSL > "$HOME/.config/starship.toml" || exit -1
}

update_vim_config() {
  mkdir -p "$HOME/.config/nvim" &&
    curl $VIM_CONFIG_URL -fsSL > "$HOME/.config/nvim/init.lua" || exit -1
  curl $VIM_RC_URL -fsSL > "$HOME/.vimrc" || exit -1
}

configure() {
  update_xshrc
  update_starship_config
  update_vim_config
}

configure
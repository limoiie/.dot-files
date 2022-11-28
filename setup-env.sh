#!/bin/bash

rawcontent=https://raw.githubusercontent.com
action=${1:-update}

curl -L $rawcontent/limoiie/.dot-files/master/setup-env-install.sh | bash -s && \
curl -L $rawcontent/limoiie/.dot-files/master/setup-env-config.sh | bash -s -- $action

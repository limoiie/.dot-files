# Dot files

This project is for sync all the limo’s dot files across machines and OSs.

Firstly, clone this project to the home path.

## Emacs dot file

The dot file for emacs is `.emacs`.
To use it, you need to:

1. Install emacs
2. Load the dot file in emacs-init-script `~/.emacs.d/init.el` (create if not exist) as:
``` lisp
(load "~/.dot-files/.emacs")
```
3. Launch emacs. The plugins will be installed automatically at the first launch. 

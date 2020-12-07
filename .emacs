;; package --- custom configuration for Emacs
;;; Commentary:
;;; Code:

;;; Initialization

(when (>= emacs-major-version 24)
  (require 'package)
  (add-to-list
   'package-archives
   '("melpa" . "https://melpa.org/packages/")
   t)
  (add-to-list
   'package-archives
   '("marmalade" . "https://marmalade-repo.org/packages/")
   t)
  (package-initialize)
  )

;; (put 'narrow-to-region 'disabled nil)


;; This is only needed once, near the top of the file
(eval-when-compile
  ;; Following line is not needed if use-package.el is in ~/.emacs.d
  ;; (add-to-list 'load-path "<path where use-package is installed>")
  (require 'use-package)
  )

;;; Use packages

(use-package compile
  :init
  (winner-mode t)
  (global-linum-mode t)
  (show-paren-mode t)
  ;; (scroll-bar-mode -1)
  (add-to-list
   'default-frame-alist
   '(font . "CodeNewRoman Nerd Font Mono-12"))
  :bind
  (("C-x 4 u" . winner-undo)
   ("C-x 4 j" . winner-redo)
   ("C-w" . (lambda ()
	      (interactive)
	      (if mark-active
		  (kill-region (region-beginning)
			       (region-end))
		(progn
		  (kill-region (line-beginning-position)
			       (line-end-position))
		  (message "Killed line")))))
   ("M-w" . (lambda ()
	      (interactive)
	      (if mark-active
		  (kill-ring-save (region-beginning)
				  (region-end))
		(progn
		  (kill-ring-save (line-beginning-position)
				  (line-end-position))
		  (message "Copied line")))))
   ("M-;" . (lambda (&optional arg)
	      (interactive "*P")
	      (comment-normalize-vars)
	      (if (and (not (region-active-p)) (not (looking-at "[ \t]*$")))
		  (comment-or-uncomment-region (line-beginning-position)
					       (line-end-position))
		(comment-dwim arg))))
   ))

(use-package window-numbering
  :ensure t
  :init
  (window-numbering-mode t))

(use-package vimish-fold
  :ensure t
  :custom
  (vimish-fold-dir (expand-file-name "vimish-fold/" "~/.emacs.d"))
  :config
  (vimish-fold-global-mode t)
  :bind
  ("C->" . vimish-fold-avy))

(use-package hideshow
  :commands (hs-minor-mode
	     hs-toggle-hiding)
  :functions
  vimish-fold--toggle
  :custom
  (hs-set-up-overlay
   (lambda (ov)
     "Display the overlay content in a tooltip"
     (when (eq 'code (overlay-get ov 'hs))
       (overlay-put ov 'help-echo
		    (buffer-substring (overlay-start ov)
				      (overlay-end ov)))
       )))
  :config
  (defun toggle-fold ()
    ;; ref https://www.reddit.com/r/emacs/comments/btwg00/folding_combined_hideshow_and_vimishfold/
    "Use `vimish-fold-toggle' if there's a fold else `hs-toggle-hiding' instead.
If region is active, adds or removes vimish folds."
    (interactive)
    (if (region-active-p)
        (unless
            (ignore-errors (vimish-fold (region-beginning) (region-end)))
          (vimish-fold-delete))
      (unless (delq nil (mapcar #'vimish-fold--toggle (overlays-at (point))))
        (hs-toggle-hiding))))
  :bind (("C-=" . hs-toggle-hiding)
	 ("C--" . toggle-fold))
  :hook
  (prog-mode . hs-minor-mode))

;; see also https://github.com/abo-abo/ace-window
(use-package ace-window
  :ensure t
  :bind ("M-o" . ace-window))

;; see also https://github.com/joaotavora/yasnippet
(use-package yasnippet
  :ensure t
  :init
  (yas-global-mode t))

;; see also https://github.com/abo-abo/avy
(use-package avy
  :ensure t
  :bind
  (("C-:" . avy-goto-line)
   ("C-;" . avy-goto-char)
   ("M-g e" . avy-goto-word-0)
   ("M-g w" . avy-goto-word-1)))

(use-package flycheck
  :ensure t
  :hook
  (after-init . global-flycheck-mode))

(use-package company-quickhelp
  :ensure t
  :init
  (company-quickhelp-mode t)
  )

(use-package company
  :ensure t
  :custom
  (company-show-numbers t)
  :bind
  (:map
   company-mode-map
   ("S-<tab>" . company-complete-common)
   ("C-?"     . company-manual-begin)
   :map
   company-active-map
   ("<tab>"   . company-complete-selection)
   ("C-p"     . company-select-previous)
   ("C-n"     . company-select-next))
  :hook
  (after-init . global-company-mode))

(use-package spaceline
  :ensure t
  :functions spaceline-compile
  :config
  (spaceline-spacemacs-theme)
  (spaceline-compile
    ;; left side
    '(((persp-name
	workspace-number
	window-number)
       :fallback evil-state
       :face highlight-face
       :priority 100)
      (anzu :priority 95)
      auto-compile
      ((buffer-modified buffer-size buffer-id remote-host)
       :priority 98)
      (major-mode :priority 79)
      (process :when active)
      ((flycheck-error flycheck-warning flycheck-info)
       :when active
       :priority 89)
      (minor-modes :when active
                   :priority 9)
      (mu4e-alert-segment :when active)
      (erc-track :when active)
      (version-control :when active
                       :priority 78)
      (org-pomodoro :when active)
      (org-clock :when active)
      nyan-cat)
    ;; right side
    '(which-function
      (python-pyvenv :fallback python-pyenv)
      (purpose :priority 94)
      (battery :when active)
      (selection-info :priority 95)
      input-method
      ((buffer-encoding-abbrev
	point-position
	line-column)
       :separator " | "
       :priority 96)
      (global :when active)
      (buffer-position :priority 99)
      (hud :priority 99)))
  )

(use-package slime
  :disabled
  :init
  (slime-setup)
  :custom
  (inferior-lisp-program "sbcl"))

;;; .emacs ends here

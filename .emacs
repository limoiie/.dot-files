;;; package --- custom configuration for Emacs
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
  (package-initialize))

;; This is only needed once, near the top of the file
(eval-when-compile
  ;; Following line is not needed if use-package.el is in ~/.emacs.d
  ;; (add-to-list 'load-path "<path where use-package is installed>")
  (require 'use-package)
  )

;;; Use packages

(use-package compile
  :custom
  (inhibit-startup-screen t)
  :init
  (winner-mode t)
  (global-linum-mode t)
  (show-paren-mode t)
  (electric-pair-mode t)
  (electric-quote-mode t)
  (load-theme 'atom-one-dark)
  (scroll-bar-mode -1)
  (tool-bar-mode -1)
  (set-face-attribute 'default nil :font "CodeNewRoman Nerd Font Mono-16")
  (set-face-attribute 'info-menu-header nil :font "CodeNewRoman Nerd Font Mono")
  (set-face-attribute 'info-title-1 nil :font "CodeNewRoman Nerd Font Mono")
  (set-face-attribute 'info-title-2 nil :font "CodeNewRoman Nerd Font Mono")
  (set-face-attribute 'info-title-3 nil :font "CodeNewRoman Nerd Font Mono")
  (set-face-attribute 'info-title-4 nil :font "CodeNewRoman Nerd Font Mono")
  (set-face-attribute 'mode-line nil :font "CodeNewRoman Nerd Font Mono-16")
  (set-face-attribute 'tab-line nil :font "CodeNewRoman Nerd Font Mono")
  (set-face-attribute 'tooltip nil :font "CodeNewRoman Nerd Font Mono")
  (set-face-attribute 'tab-bar nil :font "CodeNewRoman Nerd Font Mono")
  (set-face-attribute 'tab-bar-tab nil :font "CodeNewRoman Nerd Font Mono")
  (set-face-attribute 'tab-bar-tab-inactive nil :font "CodeNewRoman Nerd Font Mono")
  (set-face-attribute 'variable-pitch nil :font "CodeNewRoman Nerd Font Mono")
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
		(comment-dwim arg))))))

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
				      (overlay-end ov))))))
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
	 ("C-[ [27;6;61~" . hs-toggle-hiding)
	 ("C--" . toggle-fold)
	 ("C-[ [27;6;45~" . toggle-fold))
  :hook (prog-mode . hs-minor-mode))

;; config window navigation
(use-package window-numbering
  :ensure t
  :init
  (window-numbering-mode t))

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
   ("C-[ [27;6;59~" . avy-goto-char) ; for iterm2
   ("M-g e" . avy-goto-word-0)
   ("M-g w" . avy-goto-word-1)))

(use-package flycheck
  :ensure t
  :hook (after-init . global-flycheck-mode))


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
  :hook (after-init . global-company-mode))

(use-package company-quickhelp
  :ensure t
  :init
  (company-quickhelp-mode t))

(use-package company-auctex
  :ensure t
  :init
  (company-auctex-init))


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
      (hud :priority 99))))

(use-package slime
  :disabled
  :init
  (slime-setup)
  :custom
  (inferior-lisp-program "sbcl"))


;; see also https://jblevins.org/projects/markdown-mode/
(use-package markdown-mode
  :ensure t
  :commands (markdown-mode gfm-mode)
  :mode (("README\\.md\\'" . gfm-mode)
         ("\\.md\\'" . markdown-mode)
         ("\\.markdown\\'" . markdown-mode))
  ;; :init
  ;; (setq markdown-command "multimarkdown")
  )

;; see also https://github.com/seagle0128/grip-mode
;; preview markdown or org files with grip -- github flavored
(use-package grip-mode
  :ensure t
  :after markdown-mode
  :custom
  (grip-preview-use-webkit t)  ; use embedded webkit to preview
  :bind (:map markdown-mode-command-map
              ("g" . grip-mode))
  )


;; see also https://github.com/politza/pdf-tools
(use-package pdf-tools
  :ensure t
  :config
  (pdf-tools-install)
  (setq-default pdf-view-display-size 'fit-page)
  (setq pdf-annot-activate-created-annotations t)
  (define-key pdf-view-mode-map (kbd "C-s") 'isearch-forward)
  (define-key pdf-view-mode-map (kbd "C-r") 'isearch-backward)
  ;; automatically turns on midnight-mode for pdfs
  ;; (add-hook 'pdf-view-mode-hook (lambda () (bms/pdf-midnite-amber)))
  )


(use-package tex
  :ensure auctex
  :mode ("\\.tex\\'" . TeX-latex-mode)
  :config (progn
	    (setq TeX-source-correlate-mode t)
	    (setq TeX-source-correlate-method 'synctex)
	    (setq TeX-auto-save t)
	    (setq TeX-parse-self t)
	    (setq-default TeX-master "paper.tex")
	    (setq reftex-plug-into-AUCTeX t)
	    ;; make pdf-tool as the default pdf viewer for emacs
	    (setq TeX-view-program-selection '((output-pdf "PDF Tools"))
		  TeX-view-program-list '(("PDF Tools" TeX-pdf-tools-sync-view))
		  TeX-source-correlate-start-server t)
	    ;; Update PDF buffers after successful LaTeX runs
	    (add-hook 'TeX-after-compilation-finished-functions
		      #'TeX-revert-document-buffer)
	    ;; disable linum-mode in pdf-view-mode,
	    ;;   see also https://github.com/politza/pdf-tools#known-problems
	    (add-hook 'pdf-view-mode-hook (lambda () (linum-mode -1))))
	    ;; (add-hook 'LaTeX-mode-hook (lambda ()
	    ;; 				 (reftex-mode t)
	    ;; 				 (flyspell-mode t)))

  :hook ((LaTex-mode . reftex-mode)
	 (LaTex-mode . flyspell-mode))
  )

;;; .emacs ends here

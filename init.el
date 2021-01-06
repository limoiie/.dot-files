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
  (when (<= emacs-major-version 26)
    (package-initialize)
    )
  )

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
  (byte-compile-warnings '(cl-functions))
  (backup-by-copying-when-linked t)  ; preserve hard link from breaking when emacs edits it
  :init
  (electric-pair-mode t)
  (electric-quote-mode t)
  (global-linum-mode t)
  (menu-bar-mode -1)
  (scroll-bar-mode -1)
  (show-paren-mode t)
  (tool-bar-mode -1)
  (winner-mode t)
  (add-to-list 'default-frame-alist '(font . "CodeNewRoman Nerd Font Mono-16"))
  (set-face-attribute 'mode-line nil :font "CodeNewRoman Nerd Font Mono-16")
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
   ("C-c o" . (lambda ()
		(interactive)
		(if (active-minibuffer-window)
		    (select-window (active-minibuffer-window))
		  (error "Minibuffer is not active!"))))
   ))

(use-package doom-themes
  :ensure t
  :defines (doom-themes-neotree-file-icons)
  :custom
  (doom-themes-enable-bold t)   ; if nil, bold is universally disabled
  (doom-themes-enable-italic t) ; if nil, italics is universally disabled
  :config
  ;; Global settings (defaults)
  (load-theme 'doom-one)
  ;; Enable flashing mode-line on errors
  (doom-themes-visual-bell-config)
  ;; Enable custom neotree theme (all-the-icons must be installed!)
  (doom-themes-neotree-config)
  ;; (setq doom-themes-neotree-file-icons t)
  ;; or for treemacs users
  ;; (setq doom-themes-treemacs-theme "doom-colors") ; use the colorful treemacs theme
  ;; (doom-themes-treemacs-config)
  ;; Corrects (and improves) org-mode's native fontification.
  (doom-themes-org-config))


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
  :config
  (defun on_cpp_mode ()
    "Run on c++-mode"
    (message "flycheck on cpp mode!!!")
    (setq flycheck-gcc-language-standard "c++2a")
    (setq flycheck-clang-language-standard "c++2a")
    )
  :hook ((after-init . global-flycheck-mode)
	 (c++-mode   . on_cpp_mode))
  )

(use-package company
  :ensure t
  :custom
  (company-show-numbers t)
  :bind
  (:map
   company-mode-map
   ("C-\\" . company-complete-common)
   ("C-?"     . company-manual-begin)
   :map
   company-active-map
   ("<tab>"   . company-complete-selection)
   ("C-e"     . company-complete-selection)
   ("C-p"     . company-select-previous)
   ("C-n"     . company-select-next))
  :hook (after-init . global-company-mode))

(use-package company-quickhelp
  :ensure t
  :init
  (company-quickhelp-mode t))


(use-package all-the-icons)

(use-package doom-modeline
  :ensure t
  :custom
  (doom-modeline-minor-modes t)
  (doom-modeline-enable-word-count t)
  (doom-modeline-icon nil)
  :init
  (doom-modeline-mode t)
  )

(use-package neotree
  :custom
  (neo-window-fixed-size nil)
  :functions (on-toggle)
  :config
  (defun on-toggle ()
    (interactive)
    (neotree-toggle)
    (doom-modeline-mode t)
    )
  :bind ([f8] . on-toggle))

(use-package spaceline
  :disabled
  ;; :functions spaceline-compile
  ;; :config
  ;; (spaceline-spacemacs-theme)
  ;; (spaceline-compile
  ;;   ;; left side
  ;;   '(((persp-name
  ;; 	workspace-number
  ;; 	window-number)
  ;;      :fallback evil-state
  ;;      :face highlight-face
  ;;      :priority 100)
  ;;     (anzu :priority 95)
  ;;     auto-compile
  ;;     ((buffer-modified buffer-size buffer-id remote-host)
  ;;      :priority 98)
  ;;     (major-mode :priority 79)
  ;;     (process :when active)
  ;;     ((flycheck-error flycheck-warning flycheck-info)
  ;;      :when active
  ;;      :priority 89)
  ;;     (minor-modes :when active
  ;;                  :priority 9)
  ;;     (mu4e-alert-segment :when active)
  ;;     (erc-track :when active)
  ;;     (version-control :when active
  ;;                      :priority 78)
  ;;     (org-pomodoro :when active)
  ;;     (org-clock :when active)
  ;;     nyan-cat)
  ;;   ;; right side
  ;;   '(which-function
  ;;     (python-pyvenv :fallback python-pyenv)
  ;;     (purpose :priority 94)
  ;;     (battery :when active)
  ;;     (selection-info :priority 95)
  ;;     input-method
  ;;     ((buffer-encoding-abbrev
  ;; 	point-position
  ;; 	line-column)
  ;;      :separator " | "
  ;;      :priority 96)
  ;;     (global :when active)
  ;;     (buffer-position :priority 99)
  ;;     (hud :priority 99))
  ;;   )
  )

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
  :config
  (message "==> markdown-mode has been loaded!!!!")
  ;; :init
  ;; (setq markdown-command "multimarkdown")
  )

;; see also https://github.com/seagle0128/grip-mode
;; preview markdown or org files with grip -- github flavored
(use-package grip-mode
  :ensure t
  :after markdown-mode
  :config
  (message "==> grip-mode has been loaded!!!!")
  :custom
  (grip-preview-use-webkit t)  ; use embedded webkit to preview
  :bind (:map markdown-mode-command-map
	      ("g" . grip-mode))
  )


;; see also https://github.com/politza/pdf-tools
(use-package pdf-tools
  :ensure t
  :custom
  (pdf-annot-activate-created-annotations t)
  (pdf-view-display-size 'fit-page)
  :config
  (message "==> pdf-tools has been loaded!!!!")
  (pdf-tools-install)
  ;; disable linum-mode in pdf-view-mode,
  ;;   see also https://github.com/politza/pdf-tools#known-problems
  (add-hook 'pdf-view-mode-hook
	    (lambda ()
	      (linum-mode -1)
	      (pdf-view-midnight-minor-mode t)))
  :bind (:map pdf-view-mode-map
	      ("C-s" . 'isearch-forward)
	      ("C-r" . 'isearch-backward))
  )


(use-package company-bibtex
  :ensure t
  :defer t
  :custom
  (company-bibtex-bibliography
   '("/Users/ligengwang/Projects/tex/Ph.D-docs/ucasthesis/Biblio/ref.bib")))

(use-package company-auctex
  :ensure t
  :defer t)

(use-package tex
  :ensure auctex
  :mode ("\\.tex\\'" . TeX-latex-mode)
  :defines TeX-fold-macro-spec-list
  :functions (TeX-revert-document-buffer pdf-view-midnight-minor-mode)
  :custom
  ;; tex customization
  (TeX-source-correlate-mode t)
  (TeX-source-correlate-method 'synctex)
  (TeX-auto-save t)
  (TeX-parse-self t)
  (TeX-master "paper.tex")  ;; could setq-default be put in :custom?
  ;; reftex
  (reftex-plug-into-AUCTeX t)
  ;; pdf tools
  (TeX-view-program-selection '((output-pdf "PDF Tools")))
  (TeX-view-program-list '(("PDF Tools" TeX-pdf-tools-sync-view)))
  (TeX-source-correlate-start-server t)
  :config
  (message "==> tex has been loaded!!!!")
  (company-auctex-init)
  (add-to-list 'company-backends 'company-bibtex)
  (add-to-list 'TeX-engine-alist
	       '(xetex-tmp
		 "A TeX-engine that supports unicode content and store tmp files into ./Tmp"
		 "xetex -output-directory=Tmp"
		 "xelatex -output-directory=Tmp"
		 ConTeXt-engine))
  ;; Update PDF buffers after successful LaTeX runs
  (add-hook 'TeX-after-compilation-finished-functions
	    #'TeX-revert-document-buffer)
  (defun append-more-fold-macro ()
    "Append more fold macro rules"
    (TeX-fold-mode t)
    (add-to-list 'TeX-fold-macro-spec-list '("[cp]" ("citep")))
    (add-to-list 'TeX-fold-macro-spec-list '("[ct]" ("citet")))
    (add-to-list 'TeX-fold-macro-spec-list '("{1}[{2}]" ("env")))
    (add-to-list 'TeX-fold-macro-spec-list '("{3}[{1}]" ("multicolumn")))
    (add-to-list 'TeX-fold-macro-spec-list '("# {1}" ("section" "section*")) t)
    (add-to-list 'TeX-fold-macro-spec-list '("## {1}" ("subsection" "subsection*")) t)
    (add-to-list 'TeX-fold-macro-spec-list '("### {1}" ("subsubsection" "subsubsection*")) t)
    (TeX-fold-mode t)
    )
  ;; outline-mode is for outline the sections (hide, show, navgation)
  :bind-keymap ("C-o" . outline-mode-prefix-map)
  :hook ((LaTeX-mode . reftex-mode)
	 (LaTeX-mode . flyspell-mode)
	 (LaTeX-mode . outline-minor-mode)
	 (LaTeX-mode . append-more-fold-macro))
  )

(use-package multiple-cursors
  :ensure t
  :defer t
  :bind
  (("C-S-c C-S-c" . 'mc/edit-lines)
   ("C->" . 'mc/mark-next-like-this)
   ("C-<" . 'mc/mark-previous-like-this)
   ("C-c C-<" . 'mc/mark-all-like-this)
   )
  )

(use-package helm
  :ensure t
  :init
  (helm-mode t)
  :bind
  (("M-x"     . 'helm-M-x)
   ("C-x C-f" . 'helm-find-files)
   ("C-x r b" . 'helm-filtered-bookmarks)
   )
  )

(use-package helm-icons
  :ensure t
  :init
  (helm-icons-enable)
  )

(use-package bap-mode
  :ensure t
  :after helm
  :mode (("\\.bir\\'" . bap-mode)
	 ("\\.bil\\'" . bap-mode)
	 )
  )

(use-package ocp-indent
  :ensure t
  :defer t
  )

(use-package merlin
  ;; :after (company ocp-indent)
  :functions (opam-path recompile)
  :commands (merlin-document merlin-destruct merlin-switch-to-ml merlin-switch-to-mli)
  :init
  (defun opam-path (path)
    (let ((opam-share-dir (ignore-errors (car (process-lines "opam" "config" "var" "share")))))
      (concat opam-share-dir "/" path)))
  (add-to-list 'load-path (opam-path "emacs/site-lisp"))
  (add-to-list 'load-path (opam-path "tuareg"))
  (autoload 'merlin-mode "merlin" "Merlin mode" t)
  (require 'dot)
  :custom
  (merlin-completion-with-doc t)
  (merlin-use-auto-complete-mode nil)
  (tuareg-font-lock-symbols t)
  (merlin-command 'opam)
  (merlin-locate-preference 'mli)
  :config
  (message "==> merlin has been loaded!!!!")
  (add-to-list 'company-backends 'merlin-company-backend)
  (defun on-tuareg-mode ()
    "Run when tuareg mode is on"
    (ocp-setup-indent)
    ;; (add-hook 'before-save-hook 'ocp-indent-buffer)
    )
  (defun merlin-switch-between-ml-mli ()
    "Switch between ml and mli of the module that with the same name as the current file"
    (interactive)
    (let ((ext (file-name-extension (buffer-name)))
	  (base (file-name-base (buffer-name))))
      (if (string= ext "ml")
	   (merlin-switch-to-mli base)
	(merlin-switch-to-ml base)
	)))
  :hook ((tuareg-mode . merlin-mode)
	 (caml-mode   . merlin-mode)
	 (tuareg-mode . auto-fill-mode)
	 (tuareg-mode . on-tuareg-mode)
	 )
  :bind
  (("C-c c"   . 'recompile)
   ("C-c C-c" . 'recompile)
   :map merlin-mode-map
   ("C-c C-g C-m" . 'merlin-switch-to-ml)
   ("C-c C-g C-i" . 'merlin-switch-to-mli)
   ("C-c C-g C-g" . 'merlin-switch-between-ml-mli)
   ("M-."     . 'merlin-locate)
   ("C-c C-l" . 'merlin-locate-ident)
   ("C-c TAB" . 'company-complete)
   ("C-c C-d" . 'merlin-document)
   ("C-c d"   . 'merlin-destruct)
   )
  )

(use-package elpy
  :ensure t
  :defer t
  :init
  (advice-add 'python-mode :before 'elpy-enable))


(use-package company-irony-c-headers
  :ensure t
  )

(use-package company-irony
  :ensure t
  )

(use-package irony
  :ensure t
  :after (company-irony-c-headers company-irony)
  :config
  (add-to-list 'company-backends '(company-irony-c-headers company-irony))
  :hook ((c++-mode  . irony-mode)
	 (c-mode    . irony-mode)
	 (objc-mode . irony-mode))
  )

(use-package leetcode
  :ensure t
  :defer t
  :custom
  (leetcode-prefer-language "cpp")
  (leetcode-save-solutions t)
  (leetcode-directory "~/Projects/leetcode")
  )

;;; init.el ends here

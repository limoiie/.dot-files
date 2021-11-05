local Plug = vim.fn['plug#']

vim.call('plug#begin', '~/.config/nvim/plugged')

Plug('haya14busa/vim-easymotion')
Plug('neovim/nvim-lspconfig')
Plug('Pocco81/TrueZen.nvim')
Plug('tpope/vim-surround')

vim.call('plug#end')


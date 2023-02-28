-- First read our docs (completely) then check the example_config repo

local M = {}

M.ui = {
  theme = "catppuccin",
}

M.plugins = {
  -- override plugin config
  ["folke/which-key.nvim"] = {
    disable = false,
  },
  ["goolord/alpha-nvim"] = {
    disable = false,
  },
  ["neovim/nvim-lspconfig"] = {
    config = function()
      require "plugins.configs.lspconfig"
      require "custom.plugins.lspconfig"
    end,
  },
  -- install new plugin
  ["easymotion/vim-easymotion"] = { },
  ["jose-elias-alvarez/null-ls.nvim"] = {
    after = "nvim-lspconfig",
    config = function()
      require "custom.plugins.null-ls"
    end,
  },
  ["nvim-orgmode/orgmode"] = {
    config = function()
      require "custom.plugins.orgmode"
    end,
  },
  ["Pocco81/TrueZen.nvim"] = { },
  ["TimUntersberger/neogit"] = {
    requires = "nvim-lua/plenary.nvim",
    config = function()
      require "custom.plugins.neogit"
    end,
  },
}

M.mappings = {
  ["Pocco81/TrueZen.nvim"] = {
    n = {
      ['<leader>za'] = {":TZAtaraxis<CR>", "zen ataraxis"},
      ['<leader>zf'] = {":TZFocus<CR>", "zen focus current window"},
      ['<leader>zm'] = {":TZMinimalist<CR>", "zen minimalize"},
      ['<leader>zn'] = {":TZNarrow<CR>", "zen narrow"},
    },
    v = {
      ['<leader>zn'] = {":'<,'>TZNarrow<CR>", "zen narrow"},
    }
  }
}

vim.o.guifont = "Maple Mono NF:h15"
if vim.g.neovide then
  vim.g.neovide_remember_window_size = false
  vim.api.nvim_set_keymap('n', '<F11>', ":let g:neovide_fullscreen = !g:neovide_fullscreen<CR>", {})
end

return M

-- First read our docs (completely) then check the example_config repo

local M = {}

M.ui = {
  theme = "onedark",
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
  ["Pocco81/TrueZen.nvim"] = { },
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

return M

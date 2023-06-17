local plugins = {
  -- override plugin config
  {
    "neovim/nvim-lspconfig",
    dependencies = {
      "jose-elias-alvarez/null-ls.nvim",
      config = function()
        require "custom.configs.null-ls"
      end,
    },
    config = function()
      require "plugins.configs.lspconfig"
      require "custom.configs.lspconfig"
    end,
  },
  -- install new plugin
  { "easymotion/vim-easymotion", lazy = false, },
  {
    "github/copilot.vim",
    config = function ()
      require "custom.configs.copilot"
    end,
  },
  {
    "nvim-orgmode/orgmode",
    config = function()
      require "custom.configs.orgmode"
    end,
  },
  { "Pocco81/TrueZen.nvim" },
  {
    "TimUntersberger/neogit",
    requires = "nvim-lua/plenary.nvim",
    config = function()
      require "custom.configs.neogit"
    end,
  },
}

return plugins


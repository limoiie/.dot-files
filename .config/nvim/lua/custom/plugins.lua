local plugins = {
  -- override plugin config
  {
    "folke/which-key.nvim",
    enabled = true,
  },
  {
    "goolord/alpha-nvim",
    enabled = true,
  },
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
  { "easymotion/vim-easymotion" },
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


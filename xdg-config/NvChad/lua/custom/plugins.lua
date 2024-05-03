local plugins = {
  -- NvChad builtin plugins
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
  {
    "folke/which-key.nvim",
    disable = false,
    config = function()
      require("custom.configs.which-key")
    end,
  },
  -- Custom plugins
  { "easymotion/vim-easymotion", lazy = false, },
  {
    "folke/todo-comments.nvim",
    keys = { "<leader>T" },
    dependencies = { "nvim-lua/plenary.nvim" },
    config = function ()
      require "custom.configs.todo-comments"
    end,
  },
  {
    "folke/trouble.nvim",
    branch = "dev",
    keys = { "<leader>x" },
    cmd = { "Trouble" },
    dependencies = { "nvim-tree/nvim-web-devicons" },
    config = function ()
      require "custom.configs.trouble"
    end,
  },
  {
    "github/copilot.vim",
    config = function()
      require "custom.configs.copilot"
    end,
  },
  {
    "kylechui/nvim-surround",
    version = "*", -- Use for stability; omit to use `main` branch
    event = "VeryLazy",
    config = function()
      require "custom.configs.nvim-surround"
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

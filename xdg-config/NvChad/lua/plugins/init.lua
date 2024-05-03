return {
  {
    "stevearc/conform.nvim",
    -- event = 'BufWritePre', -- uncomment for format on save
    config = function()
      require "configs.conform"
    end,
  },

  -- Custom plugins
  {
    "neovim/nvim-lspconfig",
    dependencies = {
      "jose-elias-alvarez/null-ls.nvim",
      config = function()
        require "configs.null-ls"
      end,
    },
    config = function()
      require("nvchad.configs.lspconfig").defaults()
      require "configs.lspconfig"
    end,
  },

  { "easymotion/vim-easymotion", lazy = false },

  {
    "folke/todo-comments.nvim",
    keys = { "gt", "[t", "]t" },
    cmd = { "TodoTelescope", "TodoTrouble" },
    dependencies = { "nvim-lua/plenary.nvim" },
    config = function()
      require "configs.todo-comments"
    end,
  },

  {
    "folke/trouble.nvim",
    branch = "dev",
    keys = { "<leader>x" },
    cmd = { "Trouble" },
    dependencies = { "nvim-tree/nvim-web-devicons" },
    config = function()
      require "configs.trouble"
    end,
  },

  {
    "folke/which-key.nvim",
    disable = false,
    config = function()
      require "configs.which-key"
    end,
  },

  {
    "github/copilot.vim",
    config = function()
      require "configs.copilot"
    end,
  },

  {
    "kylechui/nvim-surround",
    version = "*", -- Use for stability; omit to use `main` branch
    event = "VeryLazy",
    config = function()
      require "configs.nvim-surround"
    end,
  },

  { "Pocco81/TrueZen.nvim" },

  -- {
  -- 	"williamboman/mason.nvim",
  -- 	opts = {
  -- 		ensure_installed = {
  -- 			"lua-language-server", "stylua",
  -- 			"html-lsp", "css-lsp" , "prettier"
  -- 		},
  -- 	},
  -- },

  {
    "nvim-treesitter/nvim-treesitter",
    opts = {
      ensure_installed = {
        "vim",
        "lua",
        "vimdoc",
        "html",
        "css",
        "haskell",
        "markdown",
        "markdown_inline",
      },
    },
  },
}

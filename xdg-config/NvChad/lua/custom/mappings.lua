local mappings = {
  -- NvChad builtin
  general = {
    n = {
      ["<leader>bb"] = { ":enew<CR>", "New buffer" },
    }
  },
  tabufline = {
    n = {
      ["<leader>bx"] = {
        function()
          require("nvchad.tabufline").close_buffer()
        end,
        "Close buffer",
      },
    }
  },
  lspconfig = {
    n = {
      ["F"] = {
        function()
          vim.diagnostic.open_float { border = "rounded" }
        end,
        "Floating diagnostic"
      },
      ["[d"] = {
        function()
          vim.diagnostic.goto_prev { float = { border = "rounded" } }
        end,
        "Previous diagnostic",
      },
      ["]d"] = {
        function()
          vim.diagnostic.goto_next { float = { border = "rounded" } }
        end,
        "Next diagnostic",
      },
    }
  },
  telescope = {
    n = {
      ["<leader>td"] = { ":Telescope diagnostics<CR>", "Diagnostics" },
      ["<leader>tk"] = { ":Telescope keymaps<CR>", "Keymaps" },
      ["<leader>tm"] = { ":Telescope man_pages<CR>", "Man Pages" },
      ["<leader>tt"] = { ":Telescope treesitter<CR>", "Treesitter Structure" },
      ["<leader>tx"] = { ":Telescope commands<CR>", "Commands" },
      ["<A-x>"] = { ":Telescope commands<CR>", "Telescope Commands" },
      -- File pickers
      ["<leader>tff"] = { ":Telescope find_files<CR>", "Find Files" },
      ["<leader>tfg"] = { ":Telescope git_files<CR>", "Git Files" },
      ["<leader>tfs"] = { ":Telescope live_grep<CR>", "Ripgrep" },
      ["<leader>tfr"] = { ":Telescope live_grep<CR>", "Ripgrep" },
      -- Git pickers
      ["<leader>tgb"] = { ":Telescope git_branches<CR>", "Git Branches" },
      ["<leader>tgc"] = { ":Telescope git_commits<CR>", "Git Commits" },
      ["<leader>tgf"] = { ":Telescope git_files<CR>", "Git Files" },
      ["<leader>tgs"] = { ":Telescope git_status<CR>", "Git Status" },
      ["<leader>tgS"] = { ":Telescope git_stash<CR>", "Git Stash" },
      -- LSP pickers
      ["<leader>tlr"] = { ":Telescope lsp_references<CR>", "References" },
      ["<leader>tlI"] = { ":Telescope lsp_incoming_calls<CR>", "Incoming Calls" },
      ["<leader>tlO"] = { ":Telescope lsp_outcoming_calls<CR>", "Outcoming Calls" },
      ["<leader>tls"] = { ":Telescope lsp_document_symbols<CR>", "Document Symbols" },
      ["<leader>tlS"] = { ":Telescope lsp_workspace_symbols<CR>", "Workspace Symbols" },
      ["<leader>tli"] = { ":Telescope lsp_implementation<CR>", "Goto Implementation" },
      ["<leader>tld"] = { ":Telescope lsp_definitions<CR>", "List Definitions" },
      ["<leader>tlD"] = { ":Telescope lsp_type_definitions<CR>", "List Type Definitions" },
    }
  },
  -- Custom
  ["folke/todo-comments.nvim"] = {
    n = {
      ["[t"] = {
        function()
          require("todo-comments").jump_prev()
        end,
        "Previous Todo",
      },
      ["]t"] = {
        function()
          require("todo-comments").jump_next()
        end,
        "Next Todo",
      },
      ["<leader>Tl"] = { ":TodoLocList<CR>", "Todo in LocList" },
      ["<leader>Tq"] = { ":TodoQuickFix<CR>", "Todo in Quickfix" },
      ["<leader>Tt"] = { ":TodoTelescope<CR>", "Todo in Telescope" },
      ["<leader>Tx"] = { ":TodoTrouble<CR>", "Todo in Trouble" },
    }
  },
  -- trouble.nvim is a panel-like UI component for showing lists including Quickfix, LocList, etc
  ["folke/trouble.nvim"] = {
    n = {
      ['<leader>xx'] = { ":Trouble<CR>", "Toggle"},
      ['<leader>xd'] = { ":Trouble diagnostics toggle filter.buf=0<CR>", "Toggle Document Diagnostics"},
      ['<leader>xD'] = { ":Trouble diagnostics toggle<CR>", "Toggle Workspace Diagnostics"},
      ['<leader>xl'] = { ":Trouble lsp toggle focus=false win.position=right<CR>", "Toggle LSP Def/Ref/..."},
      ['<leader>xL'] = { ":Trouble loclist toggle<CR>", "Toggle Loclist"},
      ['<leader>xq'] = { ":Trouble qflist toggle<CR>", "Toggle Quickfix"},
      ['<leader>xs'] = { ":Trouble symbols toggle focus=false<CR>", "Toggle Symbols"},
    }
  },
  ["Pocco81/TrueZen.nvim"] = {
    n = {
      ['<leader>za'] = { ":TZAtaraxis<CR>", "Zen ataraxis" },
      ['<leader>zf'] = { ":TZFocus<CR>", "Zen focus current window" },
      ['<leader>zm'] = { ":TZMinimalist<CR>", "Zen minimalize" },
      ['<leader>zn'] = { ":TZNarrow<CR>", "Zen narrow" },
    },
    v = {
      ['<leader>zn'] = { ":'<,'>TZNarrow<CR>", "zen narrow" },
    }
  }
}

return mappings

local mappings = {
  nvterm = {
    t = {
      ["<A-I>"] = {
        function()
          require("nvterm.terminal").toggle "float"
        end,
        "Toggle floating term"
      }
    },
    n = {
      ["<A-I>"] = {
        function ()
          require("nvterm.terminal").toggle "float"
        end,
        "Toggle floating term"
      }
    }
  },
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
  },
}

return mappings

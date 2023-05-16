-- First read our docs (completely) then check the example_config repo

local M = {}

M.ui = {
  theme = "everforest",
}

M.plugins = "custom.plugins"

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

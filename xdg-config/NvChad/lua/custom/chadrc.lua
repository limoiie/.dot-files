-- First read our docs (completely) then check the example_config repo

local M = {}

M.ui = {
  transparency = true,
  theme_toggle = { "aquarium", "one_light" },
  theme = "aquarium",
  statusline = {
    theme = "vscode_colored", -- default,vscode,vscode_colored,minimal
    separator_style = "default" -- default: round,block,arrow; minimal: round
  },
  nvdash = {
    load_on_startup = true,
  }
}

M.plugins = "custom.plugins"

M.mappings = require "custom.mappings"

return M

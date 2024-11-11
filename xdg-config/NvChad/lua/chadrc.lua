-- This file  needs to have same structure as nvconfig.lua
-- https://github.com/NvChad/NvChad/blob/v2.5/lua/nvconfig.lua

---@type ChadrcConfig
local M = {}

M.ui = {
  transparency = false,
  theme_toggle = { "bearded-arc", "bearded-arc" },
  theme = "bearded-arc",
  statusline = {
    theme = "vscode_colored", -- default,vscode,vscode_colored,minimal
    separator_style = "default", -- default: round,block,arrow; minimal: round
  },
  nvdash = {
    load_on_startup = true,
  },
  -- hl_override = {
  -- 	Comment = { italic = true },
  -- 	["@comment"] = { italic = true },
  -- },
}

return M

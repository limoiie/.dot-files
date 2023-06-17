-- First read our docs (completely) then check the example_config repo

local M = {}

M.ui = {
  theme_toggle = { "nightowl", "nightowl" },
  theme = "nightowl",
  nvdash = {
    load_on_startup = true,
  }
}

M.plugins = "custom.plugins"

M.mappings = require "custom.mappings"

return M

local present, plugin = pcall(require, "which-key")

if not present then
  return
end

plugin.register(
  {
    -- Buffer Group
    ["<leader>b"] = { name = "Buffer" },
    -- Telescope Groups
    ["<leader>t"] = { name = "Telescope" },
    ["<leader>tg"] = { name = "Git Picker" },
    ["<leader>tl"] = { name = "LSP Picker" },
    -- Trouble Group
    ["<leader>x"] = { name = "Trouble" },
    -- TrueZen Group
    ["<leader>z"] = { name = "TrueZen" },
  }
)

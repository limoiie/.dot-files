local present, plugin = pcall(require, "which-key")

if not present then
  return
end

plugin.register(
  {
    -- Buffer Group
    ["<leader>b"] = { name = "Buffer" },
    -- TodoComments Group
    ["<leader>T"] = { name = "Todo" },
    -- Telescope Groups
    ["<leader>t"] = { name = "Telescope" },
    ["<leader>tf"] = { name = "File Picker" },
    ["<leader>tg"] = { name = "Git Picker" },
    ["<leader>tl"] = { name = "LSP Picker" },
    -- Trouble Group
    ["<leader>x"] = { name = "Trouble" },
    -- TrueZen Group
    ["<leader>z"] = { name = "TrueZen" },
  }
)

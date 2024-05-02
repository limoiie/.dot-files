local present, which_key = pcall(require, "which-key")

if not present then
  return
end

which_key.register(
  {
    -- Telescope Groups
    ["<leader>t"] = { name = "Telescope" },
    ["<leader>tf"] = { name = "File Picker" },
    ["<leader>tg"] = { name = "Git Picker" },
    ["<leader>tl"] = { name = "LSP Picker" },
    -- TrueZen Group
    ["<leader>z"] = { name = "TrueZen" },
  }
)

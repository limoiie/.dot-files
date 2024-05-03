require "nvchad.mappings"

local map = vim.keymap.set
local nomap = vim.keymap.del

-- General
map("n", ";", ":", { desc = "CMD enter command mode" })
map("i", "jk", "<ESC>")

-- buffer
nomap("n", "<leader>b") -- Deprecated new buffer
nomap("n", "<leader>x") -- Deprecated del buffer
map("n", "<leader>bb", "<cmd> enew <CR>", { desc = "new buffer" })
map("n", "<leader>bx", function()
  require("nvchad.tabufline").close_buffer()
end, { desc = "close buffer" })

-- lspconfig
map("n", "F", function()
  vim.diagnostic.open_float { border = "rounded" }
end, { desc = "lsp floating diagnostic" })

-- telescope
map("n", "<leader>tt", "<cmd> Telescope <CR>", { desc = "telescope" })
map("n", "<leader>tk", "<cmd> Telescope keymaps <CR>", { desc = "telescope keymaps" })
map("n", "<leader>tx", "<cmd> Telescope commands <CR>", { desc = "telescope commands" })

map("n", "<leader>tgb", "<cmd> Telescope git_branches <CR>", { desc = "telescope git branches" })
map("n", "<leader>tgc", "<cmd> Telescope git_commits <CR>", { desc = "telescope git commits" })
map("n", "<leader>tgf", "<cmd> Telescope git_files <CR>", { desc = "telescope git files" })
map("n", "<leader>tgs", "<cmd> Telescope git_status <CR>", { desc = "telescope git status" })

map("n", "<leader>tlr", "<cmd> Telescope lsp_references <CR>", { desc = "telescope lsp references"})
map("n", "<leader>tli", "<cmd> Telescope lsp_incoming_calls <CR>", { desc = "telescope lsp in calls"})
map("n", "<leader>tlo", "<cmd> Telescope lsp_outcoming_calls <CR>", { desc = "telescope lsp out calls"})

-- folke/todo-comments.nvim
map("n", "gt", "<cmd> TodoTrouble <CR>", { desc = "list todos" })
map("n", "[t", function()
  require("todo-comments").jump_prev()
end, { desc = "prev todo" })
map("n", "]t", function()
  require("todo-comments").jump_next()
end, { desc = "next todo" })

-- folke/trouble.nvim
map("n", "<leader>xx", "<cmd> Trouble <CR>", { desc = "trouble cmds" })
map(
  "n",
  "<leader>xd",
  "<cmd> Trouble diagnostics toggle filter.buf=0 <CR>",
  { desc = "trouble toggle document diagnostics" }
)
map("n", "<leader>xD", "<cmd> Trouble diagnostics toggle <CR>", { desc = "trouble toggle workspace diagnostics" })
map(
  "n",
  "<leader>xl",
  "<cmd> Trouble lsp toggle focus=false win.position=right <CR>",
  { desc = "trouble toggle lsp def/ref/..." }
)
map("n", "<leader>xL", "<cmd> Trouble loclist toggle <CR>", { desc = "trouble toggle loclist" })
map("n", "<leader>xq", "<cmd> Trouble qflist toggle <CR>", { desc = "trouble toggle quickfix" })
map(
  "n",
  "<leader>xs",
  "<cmd> Trouble symbols toggle focus=false filter.buf=0 <CR>",
  { desc = "trouble toggle document symbols" }
)
map("n", "<leader>xs", "<cmd> Trouble symbols toggle focus=false <CR>", { desc = "trouble toggle workspace symbols" })

-- Pocco81/TrueZen.nvim
map("n", "<leader>za", "<cmd> TZAtarxis <CR>", { desc = "zen ataraxis" })
map("n", "<leader>zf", "<cmd> TZFocus <CR>", { desc = "zen focus" })
map("n", "<leader>zm", "<cmd> TZMinimalist <CR>", { desc = "zen minimalize" })
map("n", "<leader>zn", "<cmd> TZNarrow <CR>", { desc = "zen narrow" })
map("v", "<leader>zn", "<cmd> '<,'>TZNarrow <CR>", { desc = "zen narrow" })

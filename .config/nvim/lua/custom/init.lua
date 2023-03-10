vim.lsp.handlers["textDocument/publishDiagnostics"] = vim.lsp.with(
  vim.lsp.diagnostic.on_publish_diagnostics, {
    virtual_text = false,
    underline = true,
    signs = true,
  }
)

vim.api.nvim_set_keymap("n", "F", "<cmd>lua vim.diagnostic.open_float()<CR>", {noremap = true, silent = true})
vim.api.nvim_set_keymap("n", "]d", "<cmd>lua vim.diagnostic.goto_next()<CR>", {noremap = true, silent = true})
vim.api.nvim_set_keymap("n", "[d", "<cmd>lua vim.diagnostic.goto_prev()<CR>", {noremap = true, silent = true})

vim.o.guifont = "Maple Mono SC NF:h12"
if vim.g.neovide then
  vim.o.guifont = "Maple Mono NF:h15"

  vim.g.neovide_remember_window_size = false
  vim.api.nvim_set_keymap('n', '<F11>', ":let g:neovide_fullscreen = !g:neovide_fullscreen<CR>", {})
end


vim.lsp.handlers["textDocument/publishDiagnostics"] = vim.lsp.with(
  vim.lsp.diagnostic.on_publish_diagnostics, {
    virtual_text = false,
    underline = true,
    signs = true,
  }
)

vim.o.guifont = "Maple Mono NF:h15;Maple Mono SC NF:h15"
vim.wo.relativenumber = true

if vim.g.neovide then
  vim.g.neovide_input_macos_alt_is_meta = true
  vim.g.neovide_remember_window_size = false

  vim.api.nvim_set_keymap('n', '<F11>', ":let g:neovide_fullscreen = !g:neovide_fullscreen<CR>", {})
end


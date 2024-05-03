local present, plugin = pcall(require, "trouble")

if not present then
  return
end

-- See more https://github.com/folke/trouble.nvim#%EF%B8%8F-configuration
plugin.setup {
    auto_open = false, -- automatically open the list when you have diagnostics
    auto_close = false, -- automatically close the list when you have no diagnostics
    auto_preview = true, -- automatically preview the location of the diagnostic. <esc> to close preview and go back to last window
    auto_fold = false, -- automatically fold a file trouble list at creation
}

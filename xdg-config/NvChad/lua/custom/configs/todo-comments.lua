local present, plugin = pcall(require, "todo-comments")

if not present then
  return
end

-- See more https://github.com/folke/todo-comments.nvim#%EF%B8%8F-configuration
plugin.setup {}

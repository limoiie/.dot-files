local present, _ = pcall(require, "copilot")

if not present then
  return
end

vim.g.copilot_assume_mapped = true

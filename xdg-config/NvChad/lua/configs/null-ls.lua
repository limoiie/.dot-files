local present, null_ls = pcall(require, "null-ls")

if not present then
   return
end

local formatting = null_ls.builtins.formatting
local lint = null_ls.builtins.diagnostics

local sources = {
  --#region lang-conf
  --- Configure the formatter and linter for langs.
  --- Use mason to manage the formatter and linter commands for any lang.
  --- See more options on https://github.com/jose-elias-alvarez/null-ls.nvim/blob/main/doc/BUILTINS.md

  -- C, Cpp
  formatting.clang_format,
  lint.clang_check,
  lint.cppcheck,

  -- Haskell
  formatting.stylish_haskell,

  -- Lua
  formatting.stylua,

  -- Ocaml
  formatting.ocamlformat,

  -- Python
  formatting.black,
  lint.pylint,

  -- Rust
  -- Use the formatter and linter from lspconfig/rust-analyzer

  -- Shell
  formatting.shfmt,
  -- Use the linter from lspconfig/bash-language-server

  --#endregion
}

null_ls.setup {
   debug = true,
   sources = sources,
}

local present, null_ls = pcall(require, "null-ls")

if not present then
   return
end

local formatting = null_ls.builtins.formatting
local lint = null_ls.builtins.diagnostics

local sources = {
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
  -- formatting.autopep8,
  formatting.black,
  -- lint.flake8,  -- overtaken by pylint
  lint.pylint,

  -- Rust
  formatting.rustfmt,

  -- Shell
  formatting.shfmt,
  lint.shellcheck.with { diagnostics_format = "#{m} [#{c}]" },

  -- reference https://github.com/jose-elias-alvarez/null-ls.nvim/blob/main/doc/BUILTINS.md for more available sources
}

null_ls.setup {
   debug = true,
   sources = sources,
}

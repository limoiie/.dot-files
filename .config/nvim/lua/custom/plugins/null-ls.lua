local present, null_ls = pcall(require, "null-ls")

if not present then
   return
end

local b = null_ls.builtins

local sources = {
  -- C, Cpp
  b.formatting.clang_format,
  b.diagnostics.clang_check,
  b.diagnostics.cppcheck,

  -- Haskell
  b.formatting.stylish_haskell,

  -- Lua
  b.formatting.stylua,

  -- Ocaml
  b.formatting.ocamlformat,

  -- Python
  -- b.formatting.autopep8,
  b.formatting.black,
  -- b.diagnostics.flake8,  -- overtaken by pylint
  b.diagnostics.pylint,

  -- Rust
  b.formatting.rustfmt,

  -- Shell
  b.formatting.shfmt,
  b.diagnostics.shellcheck.with { diagnostics_format = "#{m} [#{c}]" },

  -- reference https://github.com/jose-elias-alvarez/null-ls.nvim/blob/main/doc/BUILTINS.md for more available sources
}

null_ls.setup {
   debug = true,
   sources = sources,
}

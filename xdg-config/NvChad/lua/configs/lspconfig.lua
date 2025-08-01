-- EXAMPLE
local on_attach = require("nvchad.configs.lspconfig").on_attach
local on_init = require("nvchad.configs.lspconfig").on_init
local capabilities = require("nvchad.configs.lspconfig").capabilities

local lspconfig = require("lspconfig")
local servers = {
  "bash-language-server", -- bash
	"clangd", -- c, cpp, objc
	"cmake", -- cmake
	"hls", -- haskell
	"marksman", -- markdown
	"ocamllsp", -- ocaml
	"pyright", -- python
	"rust_analyzer", -- rust
}

-- lsps with default config
for _, lsp in ipairs(servers) do
	lspconfig[lsp].setup({
		on_attach = on_attach,
		on_init = on_init,
		capabilities = capabilities,
	})
end

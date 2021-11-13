if exists("did_load_filetypes")
  finish
endif

augroup filetypedetect
  au! BufNewFile,BufRead *.yar,*.yara setfiletype yara
augroup END

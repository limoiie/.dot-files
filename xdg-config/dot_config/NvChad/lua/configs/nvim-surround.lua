local nvim_surround = require('nvim-surround')

nvim_surround.setup {
  keymaps = {
    -- *_cur: surround the current line
    -- *_line: put the surrounded on new line
    insert = "<C-g>s",
    insert_line = "<C-g>S",
    -- overwritten
    normal = "ms",
    normal_cur = "mss",
    normal_line = "mS",
    normal_cur_line = "mSS",
    visual = "ms",
    visual_line = "mS",
    delete = "md",
    change = "mr",
    change_line = "mR",
  }
}

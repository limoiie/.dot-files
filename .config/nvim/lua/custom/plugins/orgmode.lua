-- custom.plugins.orgmode
local orgmode = require "orgmode"

orgmode.setup_ts_grammar()

orgmode.setup {
  org_agenda_files = {'~/Projects/notes'},
  org_default_notes_file = {'~/Projects/notes/capture/note.org'}
}

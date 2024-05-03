local present, plugin = pcall(require, "orgmode")

if not present then
  return
end

plugin.setup_ts_grammar()

plugin.setup {
  org_agenda_files = {'~/Projects/notes'},
  org_default_notes_file = {'~/Projects/notes/capture/note.org'}
}

package choose

import "github.com/charmbracelet/bubbles/list"

// Options contain options to make a New model.
type Options struct {
	items           []list.Item
	Title           string
	noLimit         bool
	ShowDescription bool
	Height          int
	Space           int
}

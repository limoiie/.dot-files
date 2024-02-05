package choose

import "github.com/charmbracelet/bubbles/list"

// Options contain options to make a New model.
type Options struct {
	Items           []list.Item
	Title           string
	NoLimit         bool
	ShowDescription bool
	Height          int
	Space           int
}

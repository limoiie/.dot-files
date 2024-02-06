/*
Copyright © 2024 Mo Lee

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
*/

package choose

import (
	"github.com/charmbracelet/bubbles/key"
	"github.com/charmbracelet/bubbles/list"
	tea "github.com/charmbracelet/bubbletea"
)

// Model contains the state of this component.
type Model struct {
	list         list.Model
	delegateKeys *keyMap
	noLimit      bool
	forceQuit    bool
}

// item contains the state of one item component.
type item struct {
	title       string
	description string
	chosen      bool
}

func (m Model) Init() tea.Cmd {
	return tea.EnterAltScreen
}

func (m Model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
	switch msg := msg.(type) {
	case tea.WindowSizeMsg:
		// Adjust to window resize message
		h, v := appStyle.GetFrameSize()
		m.list.SetSize(msg.Width-h, msg.Height-v)

	case tea.KeyMsg:
		// Don't match any of the keys below if we're actively filtering.
		if m.list.FilterState() == list.Filtering {
			break
		}
		if selectedItem, ok := m.list.SelectedItem().(item); ok {
			switch {
			// Force quit
			case key.Matches(msg, m.list.KeyMap.ForceQuit):
				m.forceQuit = true
				return m, tea.Quit

			// Complete the selection
			case key.Matches(msg, m.delegateKeys.complete):
				return m, tea.Quit

			// Toggle selection
			case key.Matches(msg, m.delegateKeys.toggle):
				selectedItem.chosen = !selectedItem.chosen
				// Find the real index of the selected item as the list may be filtered
				realIdx := -1
				for i, curr := range m.list.Items() {
					if curr, ok := curr.(item); ok {
						if curr.title == selectedItem.title {
							realIdx = i
							break
						}
					}
				}
				// Update the chosen state of the real item
				if realIdx != -1 {
					cmd := m.list.SetItem(realIdx, selectedItem)
					if !m.noLimit {
						return m, tea.Quit // Single choose mode, complete once chosen
					}
					return m, cmd // No limit choose mode, continue to choose
				}
			}
		}
	}

	// This will also call our delegate's update function.
	updatedListModel, cmd := m.list.Update(msg)
	m.list = updatedListModel
	return m, cmd
}

func (m Model) View() string {
	return appStyle.Render(m.list.View())
}

func (m Model) Chosen() []string {
	var chosen []string
	for _, curr := range m.list.Items() {
		if curr, ok := curr.(item); ok {
			if curr.chosen {
				chosen = append(chosen, curr.title)
			}
		}
	}
	return chosen
}

// New returns a New model with sensible defaults.
func New(opt Options) Model {
	var delegateKeys = defaultKeyMap()

	// Setup list
	delegate := newItemDelegate(delegateKeys, opt)
	groceryList := list.New(opt.items, delegate, 0, 0)
	groceryList.Title = opt.Title
	groceryList.Styles.Title = titleStyle

	return Model{
		list:         groceryList,
		delegateKeys: delegateKeys,
		noLimit:      opt.noLimit,
		forceQuit:    false,
	}
}

func (i item) Title() string { return i.title }

func (i item) Description() string { return i.description }

func (i item) FilterValue() string { return i.title }

// NewItem returns a New item data.
func NewItem(title string, desc string) list.Item {
	return item{
		title:       title,
		description: desc,
	}
}

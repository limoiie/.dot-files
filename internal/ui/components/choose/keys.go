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
)

type keyMap struct {
	complete key.Binding
	toggle   key.Binding
}

// ShortHelp provides additional short help entries. This satisfies the
// help.KeyMap interface and is entirely optional.
func (keys keyMap) ShortHelp() []key.Binding {
	return []key.Binding{
		keys.complete,
		keys.toggle,
	}
}

// FullHelp provides additional full help entries. This satisfies the
// help.KeyMap interface and is entirely optional.
func (keys keyMap) FullHelp() [][]key.Binding {
	return [][]key.Binding{
		{
			keys.complete,
			keys.toggle,
		},
	}
}

func defaultKeyMap() *keyMap {
	return &keyMap{
		complete: key.NewBinding(
			key.WithKeys("enter"),
			key.WithHelp("enter", "complete with selections"),
		),
		toggle: key.NewBinding(
			key.WithKeys("tab", "whitespace"),
			key.WithHelp("tab", "toggle selection"),
		),
	}
}

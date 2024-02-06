package choose

import (
	"fmt"
	"io"
	"strings"

	"github.com/charmbracelet/bubbles/list"
	tea "github.com/charmbracelet/bubbletea"
	"github.com/charmbracelet/lipgloss"
	"github.com/muesli/reflow/truncate"
)

const (
	ellipsis           = "…"
	singleChosenPrefix = "> "
	alignChosenPrefix  = "  "
	chosenPrefix       = "◉ "
	unchosenPrefix     = "○ "
)

type DefaultItemStyles struct {
	list.DefaultItemStyles
}

type DefaultItemDelegate struct {
	list.DefaultDelegate
	noLimit bool
}

// Render renders the item view.
//
// This method is overridden to integrate the chosen mechanism.
func (delegate DefaultItemDelegate) Render(w io.Writer, m list.Model, index int, currItem list.Item) {
	var (
		title, desc string
		titlePrefix string
		descPrefix  string
		style       = &delegate.Styles
		isSelected  = index == m.Index()
	)

	// This component is invisible, return without render
	if m.Width() <= 0 {
		return
	}
	curr, ok := currItem.(item)
	if !ok {
		return
	}

	// Prepare chosen prefix
	title = curr.Title()
	desc = curr.Description()
	switch {
	case !delegate.noLimit && isSelected: // single choose mode, hover
		titlePrefix, descPrefix = singleChosenPrefix, alignChosenPrefix
	case !delegate.noLimit: // single choose mode
		titlePrefix, descPrefix = alignChosenPrefix, alignChosenPrefix
	case curr.chosen: // multi choose mode and has chosen
		titlePrefix, descPrefix = chosenPrefix, alignChosenPrefix
	default: // multi choose mode and has not chosen yet
		titlePrefix, descPrefix = unchosenPrefix, alignChosenPrefix
	}

	// Prevent text from exceeding list width
	textWidth := uint(
		m.Width() - len(titlePrefix) -
			style.NormalTitle.GetPaddingLeft() -
			style.NormalTitle.GetPaddingRight(),
	)
	title, desc = truncateText(title, desc, textWidth, delegate)

	// Conditions
	var (
		isFiltering   = m.FilterState() == list.Filtering
		isFilterEmpty = isFiltering && m.FilterValue() == ""
		isFiltered    = isFiltering || m.FilterState() == list.FilterApplied
	)

	// Highlight characters matched filter pattern
	if isFiltered && index < len(m.VisibleItems()) {
		// Get indices of matched characters
		matchedRunes := m.MatchesForItem(index)
		// highlight matched characters
		unmatched := style.SelectedTitle.Inline(true)
		matched := unmatched.Copy().Inherit(style.FilterMatch)
		title = lipgloss.StyleRunes(title, matchedRunes, matched, unmatched)
	}

	title = titlePrefix + title
	desc = descPrefix + desc

	// Style the view
	if isFilterEmpty {
		title = style.DimmedTitle.Render(title)
		desc = style.DimmedTitle.Render(desc)
	} else if isSelected && !isFiltering {
		title = style.SelectedTitle.Render(title)
		desc = style.SelectedDesc.Render(desc)
	} else {
		title = style.NormalTitle.Render(title)
		desc = style.NormalDesc.Render(desc)
	}

	// Draw the view
	if delegate.ShowDescription {
		_, _ = fmt.Fprintf(w, "%s\n%s", title, desc)
	} else {
		_, _ = fmt.Fprintf(w, "%s", title)
	}
}

func newItemDelegate(keys *keyMap, opt Options) list.ItemDelegate {
	delegate := DefaultItemDelegate{
		list.NewDefaultDelegate(),
		opt.noLimit,
	}
	delegate.SetHeight(opt.Height)
	delegate.SetSpacing(opt.Space)
	delegate.ShowDescription = opt.ShowDescription
	delegate.ShortHelpFunc = keys.ShortHelp
	delegate.FullHelpFunc = keys.FullHelp
	delegate.UpdateFunc = func(msg tea.Msg, m *list.Model) tea.Cmd {
		// seems no need the delegate except the helps
		return nil
	}
	return delegate
}

func truncateText(title string, desc string, textWidth uint, delegate DefaultItemDelegate) (string, string) {
	title = truncate.StringWithTail(title, textWidth, ellipsis)
	if delegate.ShowDescription {
		var lines []string
		for i, line := range strings.Split(desc, "\n") {
			if i >= delegate.Height()-1 {
				break
			}
			lines = append(lines, truncate.StringWithTail(line, textWidth, ellipsis))
		}
		desc = strings.Join(lines, "\n")
	}
	return title, desc
}

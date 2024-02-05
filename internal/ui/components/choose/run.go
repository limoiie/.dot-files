package choose

import (
	"fmt"
	"github.com/charmbracelet/bubbletea"
	"github.com/charmbracelet/lipgloss"
)

var (
	appStyle = lipgloss.NewStyle().Padding(1, 2)

	titleStyle = lipgloss.NewStyle().
			Foreground(lipgloss.Color("#FFFDF5")).
			Background(lipgloss.Color("#25A065")).
			Padding(0, 1)
)

func Run(opt Options) ([]string, error) {
	model := New(opt)
	finalModel, err := tea.NewProgram(model).Run()
	if err != nil {
		fmt.Println("Error running program:", err)
		return nil, err
	}
	if !finalModel.(Model).forceQuit {
		return finalModel.(Model).Chosen(), nil
	}
	return nil, nil
}

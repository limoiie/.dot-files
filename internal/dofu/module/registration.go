package module

import (
	"fmt"
)

type Meta struct {
	Name        string
	Description string
}

func GetAllModuleMetas() []Meta {
	//TODO
	const numItems = 24
	items := make([]Meta, numItems)
	for i := 0; i < numItems; i++ {
		items[i] = Meta{
			Name:        fmt.Sprintf("title %d", i),
			Description: fmt.Sprintf("description %d", i),
		}
	}
	return items
}

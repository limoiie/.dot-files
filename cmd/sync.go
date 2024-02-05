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

package cmd

import (
	"log"

	"github.com/charmbracelet/bubbles/list"
	"github.com/spf13/cobra"

	"dofu/internal/dofu"
	"dofu/internal/dofu/module"
	"dofu/internal/ui/components/choose"
)

// syncCmd represents the sync command
var syncCmd = &cobra.Command{
	Use:   "sync",
	Short: "A brief description of your command",
	Long: `A longer description that spans multiple lines and likely contains examples
and usage of using your command. For example:

Cobra is a CLI library for Go that empowers applications.
This application is a tool to generate the needed files
to quickly create a Cobra application.`,
	RunE: func(cmd *cobra.Command, args []string) error {
		modules, err := cmd.Flags().GetStringSlice("modules")
		if err != nil {
			log.Panicln("Failed to parse flags:", err)
			return err
		}

		if len(modules) == 0 {
			// fetch all modules
			items := make([]list.Item, 0)
			for _, meta := range module.GetAllModuleMetas() {
				items = append(items, choose.NewItem(
					meta.Name, meta.Description,
				))
			}
			// prompt user to choose
			modules, err = choose.Run(choose.Options{
				Items:           items,
				Title:           "Choose modules to sync with",
				NoLimit:         true,
				ShowDescription: true,
				Height:          2,
				Space:           0,
			})
			if err != nil {
				log.Panicln("Failed to select modules:", err)
				return err
			}
		}

		err = dofu.Sync(modules)
		if err != nil {
			log.Panicln("Failed to sync:", err)
			return err
		}

		return nil
	},
}

func init() {
	rootCmd.AddCommand(syncCmd)

	// Here you will define your flags and configuration settings.

	// Cobra supports Persistent Flags which will work for this command
	// and all subcommands, e.g.:
	// syncCmd.PersistentFlags().String("foo", "", "A help for foo")

	// Cobra supports local flags which will only run when this command
	// is called directly, e.g.:
	syncCmd.Flags().StringSliceP("modules", "m", []string{}, "")
}

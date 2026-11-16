package bank

import (
	"errors"
	"fmt"
	"maps"
	"slices"
	"strconv"
	"strings"
)

// Bank holds account balances and enforces the rules for changing them.
type Bank struct {
	balances map[string]int
}

func NewBank() *Bank {
	return &Bank{balances: map[string]int{}}
}

func (b *Bank) Open(name string) error {
	if _, ok := b.balances[name]; ok {
		return fmt.Errorf("account exists: %s", name)
	}
	b.balances[name] = 0
	return nil
}

func (b *Bank) Deposit(name string, amount int) error {
	if err := b.mustExist(name); err != nil {
		return err
	}
	b.balances[name] += amount
	return nil
}

func (b *Bank) Withdraw(name string, amount int) error {
	if err := b.mustExist(name); err != nil {
		return err
	}
	if b.balances[name] < amount {
		return fmt.Errorf("insufficient funds: %s", name)
	}
	b.balances[name] -= amount
	return nil
}

func (b *Bank) Transfer(from, to string, amount int) error {
	if err := b.mustExist(to); err != nil {
		return err
	}
	if err := b.Withdraw(from, amount); err != nil {
		return err
	}
	b.balances[to] += amount
	return nil
}

func (b *Bank) mustExist(name string) error {
	if _, ok := b.balances[name]; !ok {
		return fmt.Errorf("no such account: %s", name)
	}
	return nil
}

// Report lists every account and balance, sorted by name.
func (b *Bank) Report() string {
	var sb strings.Builder
	for _, name := range slices.Sorted(maps.Keys(b.balances)) {
		fmt.Fprintf(&sb, "%s: %d\n", name, b.balances[name])
	}
	return sb.String()
}

func parseAmount(text string) (int, error) {
	amount, err := strconv.Atoi(text)
	if err != nil || amount <= 0 {
		return 0, fmt.Errorf("bad amount: %s", text)
	}
	return amount, nil
}

// commands describes each command: how many arguments it takes and its usage line.
var commands = map[string]struct {
	args  int
	usage string
}{
	"open":     {1, "open NAME"},
	"deposit":  {2, "deposit NAME AMOUNT"},
	"withdraw": {2, "withdraw NAME AMOUNT"},
	"transfer": {3, "transfer FROM TO AMOUNT"},
}

// Execute runs one command line against the bank.
func (b *Bank) Execute(fields []string) error {
	cmd, args := fields[0], fields[1:]
	spec, known := commands[cmd]
	if !known {
		return fmt.Errorf("unknown command: %s", cmd)
	}
	if len(args) != spec.args {
		return errors.New("usage: " + spec.usage)
	}
	if cmd == "open" {
		return b.Open(args[0])
	}

	names, amountText := args[:len(args)-1], args[len(args)-1]
	for _, name := range names {
		if err := b.mustExist(name); err != nil {
			return err
		}
	}
	amount, err := parseAmount(amountText)
	if err != nil {
		return err
	}

	switch cmd {
	case "deposit":
		return b.Deposit(names[0], amount)
	case "withdraw":
		return b.Withdraw(names[0], amount)
	default:
		return b.Transfer(names[0], names[1], amount)
	}
}

// Run executes a script of bank commands and returns a report.
func Run(script string) string {
	bank := NewBank()
	var out strings.Builder
	for i, line := range strings.Split(script, "\n") {
		fields := strings.Fields(line)
		if len(fields) == 0 {
			continue
		}
		if err := bank.Execute(fields); err != nil {
			fmt.Fprintf(&out, "line %d: %v\n", i+1, err)
		}
	}
	out.WriteString(bank.Report())
	return out.String()
}

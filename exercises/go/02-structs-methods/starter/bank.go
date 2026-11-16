package bank

import (
	"sort"
	"strconv"
	"strings"
)

// Run executes a script of bank commands and returns a report.
func Run(script string) string {
	balances := map[string]int{}
	out := ""
	lines := strings.Split(script, "\n")
	for i := 0; i < len(lines); i++ {
		line := strings.TrimSpace(lines[i])
		if line == "" {
			continue
		}
		f := strings.Fields(line)
		if f[0] == "open" {
			if len(f) != 2 {
				out += "line " + strconv.Itoa(i+1) + ": usage: open NAME\n"
				continue
			}
			if _, ok := balances[f[1]]; ok {
				out += "line " + strconv.Itoa(i+1) + ": account exists: " + f[1] + "\n"
				continue
			}
			balances[f[1]] = 0
		} else if f[0] == "deposit" {
			if len(f) != 3 {
				out += "line " + strconv.Itoa(i+1) + ": usage: deposit NAME AMOUNT\n"
				continue
			}
			if _, ok := balances[f[1]]; !ok {
				out += "line " + strconv.Itoa(i+1) + ": no such account: " + f[1] + "\n"
				continue
			}
			amt, err := strconv.Atoi(f[2])
			if err != nil || amt <= 0 {
				out += "line " + strconv.Itoa(i+1) + ": bad amount: " + f[2] + "\n"
				continue
			}
			balances[f[1]] = balances[f[1]] + amt
		} else if f[0] == "withdraw" {
			if len(f) != 3 {
				out += "line " + strconv.Itoa(i+1) + ": usage: withdraw NAME AMOUNT\n"
				continue
			}
			if _, ok := balances[f[1]]; !ok {
				out += "line " + strconv.Itoa(i+1) + ": no such account: " + f[1] + "\n"
				continue
			}
			amt, err := strconv.Atoi(f[2])
			if err != nil || amt <= 0 {
				out += "line " + strconv.Itoa(i+1) + ": bad amount: " + f[2] + "\n"
				continue
			}
			if balances[f[1]] < amt {
				out += "line " + strconv.Itoa(i+1) + ": insufficient funds: " + f[1] + "\n"
				continue
			}
			balances[f[1]] = balances[f[1]] - amt
		} else if f[0] == "transfer" {
			if len(f) != 4 {
				out += "line " + strconv.Itoa(i+1) + ": usage: transfer FROM TO AMOUNT\n"
				continue
			}
			if _, ok := balances[f[1]]; !ok {
				out += "line " + strconv.Itoa(i+1) + ": no such account: " + f[1] + "\n"
				continue
			}
			if _, ok := balances[f[2]]; !ok {
				out += "line " + strconv.Itoa(i+1) + ": no such account: " + f[2] + "\n"
				continue
			}
			amt, err := strconv.Atoi(f[3])
			if err != nil || amt <= 0 {
				out += "line " + strconv.Itoa(i+1) + ": bad amount: " + f[3] + "\n"
				continue
			}
			if balances[f[1]] < amt {
				out += "line " + strconv.Itoa(i+1) + ": insufficient funds: " + f[1] + "\n"
				continue
			}
			balances[f[1]] = balances[f[1]] - amt
			balances[f[2]] = balances[f[2]] + amt
		} else {
			out += "line " + strconv.Itoa(i+1) + ": unknown command: " + f[0] + "\n"
		}
	}
	names := []string{}
	for name := range balances {
		names = append(names, name)
	}
	sort.Strings(names)
	for _, name := range names {
		out += name + ": " + strconv.Itoa(balances[name]) + "\n"
	}
	return out
}

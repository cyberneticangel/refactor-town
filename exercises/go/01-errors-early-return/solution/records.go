package records

import (
	"errors"
	"fmt"
	"strconv"
	"strings"
)

const (
	minAge = 0
	maxAge = 150
)

type Record struct {
	Name  string
	Age   int
	Email string
}

func ParseRecord(line string) (Record, error) {
	parts := strings.Split(line, ",")
	if len(parts) != 3 {
		return Record{}, fmt.Errorf("expected 3 fields, got %d", len(parts))
	}

	name := strings.TrimSpace(parts[0])
	if name == "" {
		return Record{}, errors.New("name is empty")
	}

	ageText := strings.TrimSpace(parts[1])
	age, err := strconv.Atoi(ageText)
	if err != nil {
		return Record{}, fmt.Errorf("invalid age %q: %w", ageText, err)
	}
	if age < minAge || age > maxAge {
		return Record{}, fmt.Errorf("age out of range: %d", age)
	}

	email := strings.TrimSpace(parts[2])
	if !strings.Contains(email, "@") {
		return Record{}, fmt.Errorf("invalid email %q", email)
	}

	return Record{Name: name, Age: age, Email: email}, nil
}

func ParseAll(lines []string) ([]Record, error) {
	var records []Record
	for i, line := range lines {
		rec, err := ParseRecord(line)
		if err != nil {
			return nil, fmt.Errorf("line %d: %w", i+1, err)
		}
		records = append(records, rec)
	}
	return records, nil
}

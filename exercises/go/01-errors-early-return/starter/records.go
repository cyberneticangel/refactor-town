package records

import (
	"fmt"
	"strconv"
	"strings"
)

type Record struct {
	Name  string
	Age   int
	Email string
}

func ParseRecord(line string) (Record, error) {
	parts := strings.Split(line, ",")
	if len(parts) == 3 {
		name := strings.TrimSpace(parts[0])
		if name != "" {
			ageText := strings.TrimSpace(parts[1])
			age, err := strconv.Atoi(ageText)
			if err == nil {
				if age >= 0 && age <= 150 {
					email := strings.TrimSpace(parts[2])
					if strings.Contains(email, "@") {
						return Record{Name: name, Age: age, Email: email}, nil
					} else {
						return Record{}, fmt.Errorf("invalid email %q", email)
					}
				} else {
					return Record{}, fmt.Errorf("age out of range: %d", age)
				}
			} else {
				return Record{}, fmt.Errorf("invalid age %q: %s", ageText, err.Error())
			}
		} else {
			return Record{}, fmt.Errorf("name is empty")
		}
	} else {
		return Record{}, fmt.Errorf("expected 3 fields, got %d", len(parts))
	}
}

func ParseAll(lines []string) ([]Record, error) {
	var records []Record
	for i, line := range lines {
		rec, err := ParseRecord(line)
		if err != nil {
			return nil, fmt.Errorf("line %d: %s", i+1, err.Error())
		} else {
			records = append(records, rec)
		}
	}
	return records, nil
}

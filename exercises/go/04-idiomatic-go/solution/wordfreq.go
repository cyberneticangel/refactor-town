package wordfreq

import (
	"cmp"
	"fmt"
	"slices"
	"strings"
)

type WordCount struct {
	Word  string
	Count int
}

func isWordChar(r rune) bool {
	return (r >= 'a' && r <= 'z') || r == '\''
}

// TopWords returns the n most frequent words (letters and apostrophes),
// case-insensitive, most frequent first, ties broken alphabetically.
func TopWords(text string, n int) []WordCount {
	words := strings.FieldsFunc(strings.ToLower(text), func(r rune) bool { return !isWordChar(r) })

	counts := map[string]int{}
	for _, w := range words {
		counts[w]++
	}

	result := make([]WordCount, 0, len(counts))
	for word, count := range counts {
		result = append(result, WordCount{word, count})
	}
	slices.SortFunc(result, func(a, b WordCount) int {
		return cmp.Or(cmp.Compare(b.Count, a.Count), cmp.Compare(a.Word, b.Word))
	})
	return result[:min(n, len(result))]
}

// Format renders counts as aligned lines, e.g. "the   3".
func Format(counts []WordCount) string {
	width := 0
	for _, c := range counts {
		width = max(width, len(c.Word))
	}
	var sb strings.Builder
	for _, c := range counts {
		fmt.Fprintf(&sb, "%-*s%d\n", width+2, c.Word, c.Count)
	}
	return sb.String()
}

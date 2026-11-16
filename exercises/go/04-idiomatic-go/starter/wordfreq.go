package wordfreq

import "strconv"

type WordCount struct {
	Word  string
	Count int
}

// TopWords returns the n most frequent words (letters and apostrophes),
// case-insensitive, most frequent first, ties broken alphabetically.
func TopWords(text string, n int) []WordCount {
	words := []string{}
	current := ""
	for i := 0; i < len(text); i++ {
		c := text[i]
		if c >= 'A' && c <= 'Z' {
			c = c + 32
		}
		if (c >= 'a' && c <= 'z') || c == '\'' {
			current = current + string(c)
		} else {
			if current != "" {
				words = append(words, current)
				current = ""
			}
		}
	}
	if current != "" {
		words = append(words, current)
	}

	unique := []string{}
	counts := []int{}
	for i := 0; i < len(words); i++ {
		found := -1
		for j := 0; j < len(unique); j++ {
			if unique[j] == words[i] {
				found = j
				break
			}
		}
		if found == -1 {
			unique = append(unique, words[i])
			counts = append(counts, 1)
		} else {
			counts[found] = counts[found] + 1
		}
	}

	for i := 0; i < len(unique); i++ {
		for j := 0; j < len(unique)-1-i; j++ {
			if counts[j] < counts[j+1] || (counts[j] == counts[j+1] && unique[j] > unique[j+1]) {
				counts[j], counts[j+1] = counts[j+1], counts[j]
				unique[j], unique[j+1] = unique[j+1], unique[j]
			}
		}
	}

	result := []WordCount{}
	for i := 0; i < len(unique) && i < n; i++ {
		result = append(result, WordCount{unique[i], counts[i]})
	}
	return result
}

// Format renders counts as aligned lines, e.g. "the   3".
func Format(counts []WordCount) string {
	width := 0
	for i := 0; i < len(counts); i++ {
		if len(counts[i].Word) > width {
			width = len(counts[i].Word)
		}
	}
	out := ""
	for i := 0; i < len(counts); i++ {
		out = out + counts[i].Word
		for j := len(counts[i].Word); j < width+2; j++ {
			out = out + " "
		}
		out = out + strconv.Itoa(counts[i].Count) + "\n"
	}
	return out
}

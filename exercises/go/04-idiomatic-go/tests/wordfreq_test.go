package wordfreq

import (
	"reflect"
	"testing"
)

const text = `The cat and the hat. THE CAT sat!
It's the cat's hat, isn't it? A hat; a cat.`

func TestTopWords(t *testing.T) {
	got := TopWords(text, 4)
	want := []WordCount{{"the", 4}, {"cat", 3}, {"hat", 3}, {"a", 2}}
	if !reflect.DeepEqual(got, want) {
		t.Fatalf("got %v, want %v", got, want)
	}
}

func TestApostrophesAndTies(t *testing.T) {
	got := TopWords(text, 100)
	if len(got) != 10 {
		t.Fatalf("expected 10 distinct words, got %d: %v", len(got), got)
	}
	tail := got[len(got)-5:]
	want := []WordCount{{"cat's", 1}, {"isn't", 1}, {"it", 1}, {"it's", 1}, {"sat", 1}}
	if !reflect.DeepEqual(tail, want) {
		t.Fatalf("got %v, want %v", tail, want)
	}
}

func TestEmptyAndZero(t *testing.T) {
	if got := TopWords("", 3); len(got) != 0 {
		t.Fatalf("got %v", got)
	}
	if got := TopWords("a b c", 0); len(got) != 0 {
		t.Fatalf("got %v", got)
	}
	if got := TopWords("123 !!! ...", 5); len(got) != 0 {
		t.Fatalf("got %v", got)
	}
}

func TestFormat(t *testing.T) {
	got := Format([]WordCount{{"the", 12}, {"elephant", 3}, {"a", 1}})
	want := "the       12\nelephant  3\na         1\n"
	if got != want {
		t.Fatalf("got:\n%q\nwant:\n%q", got, want)
	}
	if Format(nil) != "" {
		t.Fatal("empty format")
	}
}

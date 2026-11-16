package records

import (
	"reflect"
	"strings"
	"testing"
)

func TestParseRecordValid(t *testing.T) {
	got, err := ParseRecord("  Ada Lovelace , 36,ada@example.com ")
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	want := Record{Name: "Ada Lovelace", Age: 36, Email: "ada@example.com"}
	if got != want {
		t.Fatalf("got %+v, want %+v", got, want)
	}
}

func TestParseRecordErrors(t *testing.T) {
	cases := map[string]string{
		"just one field":         "expected 3 fields, got 1",
		"a,b,c,d":                "expected 3 fields, got 4",
		" ,30,x@y.z":             "name is empty",
		"Bob, thirty, b@x.com":   `invalid age "thirty"`,
		"Bob, 200, b@x.com":      "age out of range: 200",
		"Bob, -1, b@x.com":       "age out of range: -1",
		"Bob, 30, bob.at.x.com":  `invalid email "bob.at.x.com"`,
	}
	for input, wantMsg := range cases {
		_, err := ParseRecord(input)
		if err == nil {
			t.Errorf("%q: expected an error", input)
			continue
		}
		if !strings.Contains(err.Error(), wantMsg) {
			t.Errorf("%q: error %q should contain %q", input, err, wantMsg)
		}
	}
}

func TestBoundaryAges(t *testing.T) {
	for _, line := range []string{"A,0,a@b", "A,150,a@b"} {
		if _, err := ParseRecord(line); err != nil {
			t.Errorf("%q should be valid: %v", line, err)
		}
	}
}

func TestParseAll(t *testing.T) {
	got, err := ParseAll([]string{"A,1,a@x", "B,2,b@x"})
	if err != nil {
		t.Fatal(err)
	}
	want := []Record{{"A", 1, "a@x"}, {"B", 2, "b@x"}}
	if !reflect.DeepEqual(got, want) {
		t.Fatalf("got %+v", got)
	}
}

func TestParseAllReportsLine(t *testing.T) {
	_, err := ParseAll([]string{"A,1,a@x", "B,2,b@x", "C,old,c@x"})
	if err == nil || !strings.HasPrefix(err.Error(), `line 3: invalid age "old"`) {
		t.Fatalf("got %v", err)
	}
}

func TestParseAllEmpty(t *testing.T) {
	got, err := ParseAll(nil)
	if err != nil || len(got) != 0 {
		t.Fatalf("got %v, %v", got, err)
	}
}

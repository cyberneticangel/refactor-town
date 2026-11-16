package bank

import "testing"

func TestHappyPath(t *testing.T) {
	got := Run(`
open alice
open bob
deposit alice 100
withdraw alice 30
transfer alice bob 20
deposit bob 5
`)
	want := "alice: 50\nbob: 25\n"
	if got != want {
		t.Fatalf("got:\n%s\nwant:\n%s", got, want)
	}
}

func TestErrorsAreReportedWithLineNumbers(t *testing.T) {
	got := Run(`open alice
open alice
deposit carol 10
deposit alice ten
deposit alice -5
withdraw alice 1
transfer alice bob 1
transfer alice
fly alice
open
deposit alice 7`)
	want := "" +
		"line 2: account exists: alice\n" +
		"line 3: no such account: carol\n" +
		"line 4: bad amount: ten\n" +
		"line 5: bad amount: -5\n" +
		"line 6: insufficient funds: alice\n" +
		"line 7: no such account: bob\n" +
		"line 8: usage: transfer FROM TO AMOUNT\n" +
		"line 9: unknown command: fly\n" +
		"line 10: usage: open NAME\n" +
		"alice: 7\n"
	if got != want {
		t.Fatalf("got:\n%s\nwant:\n%s", got, want)
	}
}

func TestErrorPriority(t *testing.T) {
	// unknown account is reported before a bad amount; source before destination
	got := Run("open a\ntransfer x y zero\ntransfer a y zero\ntransfer a a zero\nwithdraw a 0")
	want := "line 2: no such account: x\nline 3: no such account: y\nline 4: bad amount: zero\nline 5: bad amount: 0\na: 0\n"
	if got != want {
		t.Fatalf("got:\n%s\nwant:\n%s", got, want)
	}
}

func TestFailedTransferChangesNothing(t *testing.T) {
	got := Run("open a\nopen b\ndeposit a 10\ntransfer a b 11")
	want := "line 4: insufficient funds: a\na: 10\nb: 0\n"
	if got != want {
		t.Fatalf("got:\n%s\nwant:\n%s", got, want)
	}
}

func TestEmptyScript(t *testing.T) {
	if got := Run(""); got != "" {
		t.Fatalf("got %q", got)
	}
}

func TestSortedReport(t *testing.T) {
	got := Run("open zed\nopen amy\nopen mo")
	if got != "amy: 0\nmo: 0\nzed: 0\n" {
		t.Fatalf("got %q", got)
	}
}

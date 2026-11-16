package payments

import (
	"math"
	"testing"
)

func near(a, b float64) bool { return math.Abs(a-b) < 1e-9 }

func TestFees(t *testing.T) {
	cases := []struct {
		p   Payment
		fee float64
	}{
		{NewCard(100, "4242"), 3.20},
		{NewPayPal(100, "ada@example.com"), 3.98},
		{NewCrypto(100, "0xdeadbeef"), 1.00},
		{NewCard(0, "0000"), 0.30},
	}
	for _, c := range cases {
		if !near(c.p.Fee(), c.fee) {
			t.Errorf("%s: fee %.4f, want %.4f", c.p.Describe(), c.p.Fee(), c.fee)
		}
	}
}

func TestDescribe(t *testing.T) {
	cases := map[string]Payment{
		"card ****4242: $10.00 (fee $0.59)":         NewCard(10, "4242"),
		"paypal ada@example.com: $20.00 (fee $1.19)": NewPayPal(20, "ada@example.com"),
		"crypto 0xdead…: $5.50 (fee $1.00)":          NewCrypto(5.5, "0xdeadbeef"),
		"crypto 0xab: $1.00 (fee $1.00)":             NewCrypto(1, "0xab"),
	}
	for want, p := range cases {
		if got := p.Describe(); got != want {
			t.Errorf("got %q, want %q", got, want)
		}
	}
}

func TestTotal(t *testing.T) {
	ps := []Payment{NewCard(100, "4242"), NewPayPal(100, "a@b"), NewCrypto(100, "w")}
	if got := Total(ps); !near(got, 308.18) {
		t.Fatalf("total %.4f", got)
	}
	if Total(nil) != 0 {
		t.Fatal("empty total should be 0")
	}
}

func TestAmount(t *testing.T) {
	if NewPayPal(12.5, "x@y").Amount() != 12.5 {
		t.Fatal("amount")
	}
}

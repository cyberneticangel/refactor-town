package payments

import "fmt"

// Payment is anything that has an amount, charges a fee and can describe itself.
// Each payment method is its own type; nobody switches on a "kind" string.
type Payment interface {
	Amount() float64
	Fee() float64
	Describe() string
}

type Card struct {
	amount float64
	last4  string
}

type PayPal struct {
	amount float64
	email  string
}

type Crypto struct {
	amount float64
	wallet string
}

func NewCard(amount float64, last4 string) Payment    { return Card{amount, last4} }
func NewPayPal(amount float64, email string) Payment  { return PayPal{amount, email} }
func NewCrypto(amount float64, wallet string) Payment { return Crypto{amount, wallet} }

func (c Card) Amount() float64 { return c.amount }
func (c Card) Fee() float64    { return 0.30 + c.amount*0.029 }
func (c Card) Describe() string {
	return describe("card ****"+c.last4, c)
}

func (p PayPal) Amount() float64 { return p.amount }
func (p PayPal) Fee() float64    { return 0.49 + p.amount*0.0349 }
func (p PayPal) Describe() string {
	return describe("paypal "+p.email, p)
}

func (c Crypto) Amount() float64 { return c.amount }
func (c Crypto) Fee() float64    { return 1.00 }
func (c Crypto) Describe() string {
	short := c.wallet
	if len(short) > 6 {
		short = short[:6] + "…"
	}
	return describe("crypto "+short, c)
}

// describe holds the formatting every payment shares.
func describe(label string, p Payment) string {
	return fmt.Sprintf("%s: $%.2f (fee $%.2f)", label, p.Amount(), p.Fee())
}

func Total(payments []Payment) float64 {
	total := 0.0
	for _, p := range payments {
		total += p.Amount() + p.Fee()
	}
	return total
}

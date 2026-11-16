package payments

import "fmt"

type Payment struct {
	kind   string
	amount float64
	last4  string // only used by cards
	email  string // only used by paypal
	wallet string // only used by crypto
}

func NewCard(amount float64, last4 string) Payment {
	return Payment{kind: "card", amount: amount, last4: last4}
}

func NewPayPal(amount float64, email string) Payment {
	return Payment{kind: "paypal", amount: amount, email: email}
}

func NewCrypto(amount float64, wallet string) Payment {
	return Payment{kind: "crypto", amount: amount, wallet: wallet}
}

func (p Payment) Amount() float64 {
	return p.amount
}

func (p Payment) Fee() float64 {
	switch p.kind {
	case "card":
		return 0.30 + p.amount*0.029
	case "paypal":
		return 0.49 + p.amount*0.0349
	case "crypto":
		return 1.00
	default:
		panic("unknown payment kind " + p.kind)
	}
}

func (p Payment) Describe() string {
	switch p.kind {
	case "card":
		return fmt.Sprintf("card ****%s: $%.2f (fee $%.2f)", p.last4, p.amount, p.Fee())
	case "paypal":
		return fmt.Sprintf("paypal %s: $%.2f (fee $%.2f)", p.email, p.amount, p.Fee())
	case "crypto":
		short := p.wallet
		if len(short) > 6 {
			short = short[:6] + "…"
		}
		return fmt.Sprintf("crypto %s: $%.2f (fee $%.2f)", short, p.amount, p.Fee())
	default:
		panic("unknown payment kind " + p.kind)
	}
}

func Total(payments []Payment) float64 {
	total := 0.0
	for _, p := range payments {
		total += p.Amount() + p.Fee()
	}
	return total
}

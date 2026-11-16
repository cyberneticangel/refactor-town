# country: (base fee, price per kg, express surcharge)
RATES = {
    "US": (5.00, 1.50, 10.00),
    "CA": (8.00, 2.00, 15.00),
    "MX": (9.00, 2.25, 20.00),
}
MEMBER_DISCOUNT = 0.10
DISCOUNT_THRESHOLD = 50


def shipping_cost(weight, country, express, member):
    if weight <= 0:
        raise ValueError("weight must be positive")
    if country not in RATES:
        raise ValueError("unsupported country: " + country)

    base, per_kg, express_fee = RATES[country]
    cost = base + weight * per_kg
    if express:
        cost += express_fee
    if member and cost > DISCOUNT_THRESHOLD:
        cost *= 1 - MEMBER_DISCOUNT
    return round(cost, 2)

def shipping_cost(weight, country, express, member):
    if weight > 0:
        if country == "US":
            if express:
                cost = 5.00 + weight * 1.50 + 10.00
            else:
                cost = 5.00 + weight * 1.50
        else:
            if country == "CA":
                if express:
                    cost = 8.00 + weight * 2.00 + 15.00
                else:
                    cost = 8.00 + weight * 2.00
            else:
                if country == "MX":
                    if express:
                        cost = 9.00 + weight * 2.25 + 20.00
                    else:
                        cost = 9.00 + weight * 2.25
                else:
                    raise ValueError("unsupported country: " + country)
        if member:
            if cost > 50:
                cost = cost * 0.9
        return round(cost, 2)
    else:
        raise ValueError("weight must be positive")

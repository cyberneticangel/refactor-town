def build_report(orders):
    lines = []

    lines.append("=== PENDING ===")
    total = 0
    for o in orders:
        if o["status"] == "pending":
            lines.append(f"{o['id']:>5} | {o['customer']:<12} | ${o['amount']:>8.2f}")
            total = total + o["amount"]
    lines.append(f"{'TOTAL':>5} | {'':<12} | ${total:>8.2f}")
    lines.append("")

    lines.append("=== SHIPPED ===")
    total = 0
    for o in orders:
        if o["status"] == "shipped":
            lines.append(f"{o['id']:>5} | {o['customer']:<12} | ${o['amount']:>8.2f}")
            total = total + o["amount"]
    lines.append(f"{'TOTAL':>5} | {'':<12} | ${total:>8.2f}")
    lines.append("")

    lines.append("=== DELIVERED ===")
    total = 0
    for o in orders:
        if o["status"] == "delivered":
            lines.append(f"{o['id']:>5} | {o['customer']:<12} | ${o['amount']:>8.2f}")
            total = total + o["amount"]
    lines.append(f"{'TOTAL':>5} | {'':<12} | ${total:>8.2f}")
    lines.append("")

    return "\n".join(lines)

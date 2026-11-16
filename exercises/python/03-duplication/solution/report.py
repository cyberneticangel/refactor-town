STATUSES = ("pending", "shipped", "delivered")


def format_row(label, name, amount):
    return f"{label:>5} | {name:<12} | ${amount:>8.2f}"


def build_section(orders, status):
    matching = [order for order in orders if order["status"] == status]
    lines = [f"=== {status.upper()} ==="]
    lines += [format_row(o["id"], o["customer"], o["amount"]) for o in matching]
    lines.append(format_row("TOTAL", "", sum(o["amount"] for o in matching)))
    lines.append("")
    return lines


def build_report(orders):
    lines = []
    for status in STATUSES:
        lines += build_section(orders, status)
    return "\n".join(lines)

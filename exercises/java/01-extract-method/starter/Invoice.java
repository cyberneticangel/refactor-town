import java.util.List;

public class Invoice {
    private final String customer;
    private final List<LineItem> items;

    public Invoice(String customer, List<LineItem> items) {
        this.customer = customer;
        this.items = items;
    }

    public String render() {
        StringBuilder sb = new StringBuilder();
        sb.append("INVOICE for ").append(customer).append("\n");
        double subtotal = 0;
        for (LineItem item : items) {
            double lineTotal = item.quantity() * item.unitPrice();
            String note = "";
            if (item.quantity() >= 10) {
                lineTotal = lineTotal * 0.9;
                note = "  (bulk -10%)";
            }
            subtotal += lineTotal;
            sb.append(String.format("  %-10s x%3d @ %7.2f = %8.2f%s%n",
                    item.name(), item.quantity(), item.unitPrice(), lineTotal, note));
        }
        double tax = subtotal * 0.0825;
        double shipping;
        if (subtotal >= 100) {
            shipping = 0;
        } else {
            shipping = 7.99;
        }
        if (items.isEmpty()) {
            shipping = 0;
        }
        double total = subtotal + tax + shipping;
        sb.append(String.format("%-10s %10.2f%n", "Subtotal:", subtotal));
        sb.append(String.format("%-10s %10.2f%n", "Tax:", tax));
        sb.append(String.format("%-10s %10.2f%n", "Shipping:", shipping));
        sb.append(String.format("%-10s %10.2f%n", "Total:", total));
        return sb.toString();
    }

    public double total() {
        double subtotal = 0;
        for (LineItem item : items) {
            double lineTotal = item.quantity() * item.unitPrice();
            if (item.quantity() >= 10) {
                lineTotal = lineTotal * 0.9;
            }
            subtotal += lineTotal;
        }
        double tax = subtotal * 0.0825;
        double shipping = subtotal >= 100 ? 0 : 7.99;
        if (items.isEmpty()) {
            shipping = 0;
        }
        return subtotal + tax + shipping;
    }
}

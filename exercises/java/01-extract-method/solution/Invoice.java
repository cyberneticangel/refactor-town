import java.util.List;

public class Invoice {
    private static final double TAX_RATE = 0.0825;
    private static final int BULK_QUANTITY = 10;
    private static final double BULK_DISCOUNT = 0.10;
    private static final double FREE_SHIPPING_FROM = 100;
    private static final double SHIPPING_FEE = 7.99;

    private final String customer;
    private final List<LineItem> items;

    public Invoice(String customer, List<LineItem> items) {
        this.customer = customer;
        this.items = items;
    }

    private static boolean isBulk(LineItem item) {
        return item.quantity() >= BULK_QUANTITY;
    }

    private static double lineTotal(LineItem item) {
        double gross = item.quantity() * item.unitPrice();
        return isBulk(item) ? gross * (1 - BULK_DISCOUNT) : gross;
    }

    private double subtotal() {
        return items.stream().mapToDouble(Invoice::lineTotal).sum();
    }

    private double tax() {
        return subtotal() * TAX_RATE;
    }

    private double shipping() {
        if (items.isEmpty() || subtotal() >= FREE_SHIPPING_FROM) {
            return 0;
        }
        return SHIPPING_FEE;
    }

    public double total() {
        return subtotal() + tax() + shipping();
    }

    private static String formatLine(LineItem item) {
        String note = isBulk(item) ? "  (bulk -10%)" : "";
        return String.format("  %-10s x%3d @ %7.2f = %8.2f%s%n",
                item.name(), item.quantity(), item.unitPrice(), lineTotal(item), note);
    }

    private static String formatSummary(String label, double amount) {
        return String.format("%-10s %10.2f%n", label, amount);
    }

    public String render() {
        StringBuilder sb = new StringBuilder("INVOICE for " + customer + "\n");
        items.forEach(item -> sb.append(formatLine(item)));
        sb.append(formatSummary("Subtotal:", subtotal()));
        sb.append(formatSummary("Tax:", tax()));
        sb.append(formatSummary("Shipping:", shipping()));
        sb.append(formatSummary("Total:", total()));
        return sb.toString();
    }
}

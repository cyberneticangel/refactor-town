public record Contractor(String name, double invoiceTotal) implements Employee {
    public String kind() {
        return "contractor";
    }

    public double monthlyPay() {
        return invoiceTotal;
    }
}

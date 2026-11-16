public record Salaried(String name, double annualSalary) implements Employee {
    public String kind() {
        return "salaried";
    }

    public double monthlyPay() {
        return annualSalary / 12;
    }
}

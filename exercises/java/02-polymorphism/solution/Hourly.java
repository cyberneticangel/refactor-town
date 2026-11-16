public record Hourly(String name, double hourlyRate, int hours) implements Employee {
    private static final int STANDARD_HOURS = 160;
    private static final double OVERTIME_MULTIPLIER = 1.5;

    public String kind() {
        return "hourly";
    }

    public double monthlyPay() {
        int overtime = Math.max(0, hours - STANDARD_HOURS);
        int regular = hours - overtime;
        return hourlyRate * (regular + overtime * OVERTIME_MULTIPLIER);
    }
}

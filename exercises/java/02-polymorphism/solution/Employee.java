/** Anyone we pay. Each kind of employee knows how its own pay works. */
public interface Employee {
    String name();

    String kind();

    double monthlyPay();

    default String payslip() {
        return String.format("%s (%s): $%.2f", name(), kind(), monthlyPay());
    }
}

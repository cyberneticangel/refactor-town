import java.util.List;

public class Payroll {
    public static double monthlyPay(Employee employee) {
        return employee.monthlyPay();
    }

    public static String payslip(Employee employee) {
        return employee.payslip();
    }

    public static double total(List<? extends Employee> staff) {
        return staff.stream().mapToDouble(Employee::monthlyPay).sum();
    }
}

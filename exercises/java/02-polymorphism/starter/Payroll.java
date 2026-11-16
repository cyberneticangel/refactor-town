import java.util.List;

public class Payroll {
    public static double monthlyPay(Object employee) {
        if (employee instanceof Salaried) {
            Salaried s = (Salaried) employee;
            return s.annualSalary / 12;
        } else if (employee instanceof Hourly) {
            Hourly h = (Hourly) employee;
            double pay = h.hourlyRate * Math.min(h.hours, 160);
            if (h.hours > 160) {
                pay += (h.hours - 160) * h.hourlyRate * 1.5;
            }
            return pay;
        } else if (employee instanceof Contractor) {
            Contractor c = (Contractor) employee;
            return c.invoiceTotal;
        } else {
            throw new IllegalArgumentException("unknown employee type");
        }
    }

    public static String payslip(Object employee) {
        String name;
        String kind;
        if (employee instanceof Salaried) {
            name = ((Salaried) employee).name;
            kind = "salaried";
        } else if (employee instanceof Hourly) {
            name = ((Hourly) employee).name;
            kind = "hourly";
        } else if (employee instanceof Contractor) {
            name = ((Contractor) employee).name;
            kind = "contractor";
        } else {
            throw new IllegalArgumentException("unknown employee type");
        }
        return String.format("%s (%s): $%.2f", name, kind, monthlyPay(employee));
    }

    public static double total(List<?> staff) {
        double sum = 0;
        for (Object e : staff) {
            sum += monthlyPay(e);
        }
        return sum;
    }
}

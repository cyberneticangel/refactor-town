import java.util.*;

public class Tests {
    // ---- tiny test runner -------------------------------------------------
    static int passed = 0, failed = 0;

    interface Body { void run() throws Exception; }

    static void test(String name, Body body) {
        try {
            body.run();
            passed++;
            System.out.println("  ok   " + name);
        } catch (Throwable t) {
            failed++;
            System.out.println("  FAIL " + name + "\n       " + t);
        }
    }

    static void eq(Object expected, Object actual) {
        if (!Objects.equals(expected, actual)) {
            throw new AssertionError("expected:\n" + expected + "\n       but got:\n" + actual);
        }
    }

    static void near(double expected, double actual) {
        if (Math.abs(expected - actual) > 1e-6) throw new AssertionError("expected " + expected + " but got " + actual);
    }

    static void finish() {
        System.out.println("\n" + passed + " passed, " + failed + " failed");
        System.exit(failed == 0 ? 0 : 1);
    }
    // ------------------------------------------------------------------------


    public static void main(String[] args) {
        var ann = new Salaried("Ann", 60000);
        var bo = new Hourly("Bo", 20.0, 170);
        var cy = new Contractor("Cy", 4500);

        test("salaried pay is a twelfth of the salary", () -> near(5000, Payroll.monthlyPay(ann)));
        test("hourly pay includes overtime past 160h", () -> {
            near(3500, Payroll.monthlyPay(bo));
            near(2000, Payroll.monthlyPay(new Hourly("Di", 20.0, 100)));
            near(3200, Payroll.monthlyPay(new Hourly("Ed", 20.0, 160)));
        });
        test("contractors are paid their invoice", () -> near(4500, Payroll.monthlyPay(cy)));
        test("payslips", () -> {
            eq("Ann (salaried): $5000.00", Payroll.payslip(ann));
            eq("Bo (hourly): $3500.00", Payroll.payslip(bo));
            eq("Cy (contractor): $4500.00", Payroll.payslip(cy));
        });
        test("total", () -> {
            near(13000, Payroll.total(List.of(ann, bo, cy)));
            near(0, Payroll.total(List.of()));
        });
        finish();
    }
}

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


    static final List<Sale> SALES = List.of(
            new Sale("North", "Widget", 120.0),
            new Sale("South", "Gadget", 75.5),
            new Sale("North", "Gadget", 30.0),
            new Sale("East", "Widget", 200.0),
            new Sale("South", "Widget", 10.0),
            new Sale("East", "Doohickey", 105.5),
            new Sale("North", "Gizmo", 105.5));

    public static void main(String[] args) {
        test("totals by region, sorted", () -> {
            Map<String, Double> t = SalesReport.totalByRegion(SALES);
            eq(List.of("East", "North", "South"), new ArrayList<>(t.keySet()));
            near(305.5, t.get("East"));
            near(255.5, t.get("North"));
            near(85.5, t.get("South"));
            eq(Map.of(), SalesReport.totalByRegion(List.of()));
        });
        test("top products with alphabetical tie-break", () -> {
            eq(List.of("Widget", "Doohickey"), SalesReport.topProducts(SALES, 2));  // three-way tie at 105.50
            eq(List.of("Widget", "Doohickey", "Gadget", "Gizmo"), SalesReport.topProducts(SALES, 10));
            eq(List.of(), SalesReport.topProducts(SALES, 0));
        });
        test("average above threshold", () -> {
            near((120 + 200 + 105.5 + 105.5) / 4, SalesReport.averageAbove(SALES, 100));
            near(0, SalesReport.averageAbove(SALES, 1000));
            near(0, SalesReport.averageAbove(SALES, 200));
        });
        test("regions selling a product", () -> {
            eq(List.of("East", "North", "South"), SalesReport.regionsSelling(SALES, "Widget"));
            eq(List.of("North"), SalesReport.regionsSelling(SALES, "Gizmo"));
            eq(List.of(), SalesReport.regionsSelling(SALES, "Nothing"));
        });
        finish();
    }
}

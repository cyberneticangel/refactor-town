import java.util.List;
import java.util.Objects;

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
    // ------------------------------------------------------------------------

    static final Invoice SMALL = new Invoice("ACME", List.of(new LineItem("Pen", 12, 1.50), new LineItem("Notebook", 2, 4.00)));
    static final Invoice BIG = new Invoice("Globex", List.of(new LineItem("Monitor", 1, 180.00), new LineItem("Cable", 10, 2.00)));
    static final Invoice EMPTY = new Invoice("Nobody", List.of());

    public static void main(String[] args) {
        test("small order renders with shipping and bulk discount", () -> eq("""
                INVOICE for ACME
                  Pen        x 12 @    1.50 =    16.20  (bulk -10%)
                  Notebook   x  2 @    4.00 =     8.00
                Subtotal:       24.20
                Tax:             2.00
                Shipping:        7.99
                Total:          34.19
                """, SMALL.render()));

        test("large order ships free", () -> eq("""
                INVOICE for Globex
                  Monitor    x  1 @  180.00 =   180.00
                  Cable      x 10 @    2.00 =    18.00  (bulk -10%)
                Subtotal:      198.00
                Tax:            16.34
                Shipping:        0.00
                Total:         214.34
                """, BIG.render()));

        test("empty invoice", () -> eq("""
                INVOICE for Nobody
                Subtotal:        0.00
                Tax:             0.00
                Shipping:        0.00
                Total:           0.00
                """, EMPTY.render()));

        test("total() matches the rendered total", () -> {
            near(34.1865, SMALL.total());
            near(214.335, BIG.total());
            near(0.0, EMPTY.total());
        });

        test("free shipping starts at exactly 100", () ->
                near(100 * 1.0825, new Invoice("X", List.of(new LineItem("Thing", 1, 100.0))).total()));

        test("bulk starts at exactly 10", () -> {
            near(9 * 1.0825 + 7.99, new Invoice("X", List.of(new LineItem("A", 9, 1.0))).total());
            near(9 * 1.0825 + 7.99, new Invoice("X", List.of(new LineItem("A", 10, 1.0))).total());
        });

        System.out.println("\n" + passed + " passed, " + failed + " failed");
        System.exit(failed == 0 ? 0 : 1);
    }
}

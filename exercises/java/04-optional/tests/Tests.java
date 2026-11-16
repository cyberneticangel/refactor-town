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
        UserDirectory dir = new UserDirectory();
        dir.add("u1", "Ada", "ada@Example.COM");
        dir.add("u2", "Brian", null);
        dir.add("u3", "Cleo", "   ");
        dir.add("u4", "Dev", "dev-at-nowhere");

        test("contact lines", () -> {
            eq("Ada <ada@Example.COM>", dir.contactLine("u1"));
            eq("Brian (no email)", dir.contactLine("u2"));
            eq("Cleo (no email)", dir.contactLine("u3"));
            eq("Dev <dev-at-nowhere>", dir.contactLine("u4"));
            eq("unknown user", dir.contactLine("nobody"));
        });
        test("domains", () -> {
            eq("example.com", dir.domainOf("u1"));
            eq("n/a", dir.domainOf("u2"));
            eq("n/a", dir.domainOf("u3"));
            eq("n/a", dir.domainOf("u4"));
            eq("n/a", dir.domainOf("nobody"));
        });
        test("count with email", () -> {
            eq(2, dir.countWithEmail());
            eq(0, new UserDirectory().countWithEmail());
        });
        test("re-adding replaces", () -> {
            UserDirectory d = new UserDirectory();
            d.add("x", "Xi", null);
            d.add("x", "Xi", "xi@x.org");
            eq("x.org", d.domainOf("x"));
            eq(1, d.countWithEmail());
        });
        finish();
    }
}

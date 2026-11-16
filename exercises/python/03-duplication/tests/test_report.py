import unittest

from report import build_report

ORDERS = [
    {"id": 101, "customer": "Ada", "amount": 25.5, "status": "pending"},
    {"id": 102, "customer": "Grace", "amount": 1200.0, "status": "shipped"},
    {"id": 103, "customer": "Linus", "amount": 9.99, "status": "pending"},
    {"id": 104, "customer": "Margaret", "amount": 310.25, "status": "delivered"},
    {"id": 105, "customer": "Dennis", "amount": 42.0, "status": "cancelled"},
]

EXPECTED = """=== PENDING ===
  101 | Ada          | $   25.50
  103 | Linus        | $    9.99
TOTAL |              | $   35.49

=== SHIPPED ===
  102 | Grace        | $ 1200.00
TOTAL |              | $ 1200.00

=== DELIVERED ===
  104 | Margaret     | $  310.25
TOTAL |              | $  310.25
"""


class ReportTests(unittest.TestCase):
    def test_full_report(self):
        self.assertEqual(build_report(ORDERS), EXPECTED)

    def test_unknown_statuses_are_skipped(self):
        self.assertNotIn("Dennis", build_report(ORDERS))

    def test_empty_sections_still_have_totals(self):
        report = build_report([])
        self.assertEqual(report.count("TOTAL"), 3)
        self.assertIn("$    0.00", report)

    def test_order_within_section_is_preserved(self):
        report = build_report(ORDERS)
        self.assertLess(report.index("Ada"), report.index("Linus"))


if __name__ == "__main__":
    unittest.main()

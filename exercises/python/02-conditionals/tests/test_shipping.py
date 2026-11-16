import unittest

from shipping import shipping_cost


class ShippingTests(unittest.TestCase):
    def test_standard_rates(self):
        self.assertAlmostEqual(shipping_cost(2, "US", False, False), 8.00)
        self.assertAlmostEqual(shipping_cost(2, "CA", False, False), 12.00)
        self.assertAlmostEqual(shipping_cost(2, "MX", False, False), 13.50)

    def test_express_surcharge(self):
        self.assertAlmostEqual(shipping_cost(2, "US", True, False), 18.00)
        self.assertAlmostEqual(shipping_cost(2, "CA", True, False), 27.00)
        self.assertAlmostEqual(shipping_cost(2, "MX", True, False), 33.50)

    def test_member_discount_only_above_threshold(self):
        self.assertAlmostEqual(shipping_cost(2, "US", False, True), 8.00)
        self.assertAlmostEqual(shipping_cost(30, "US", False, True), 50.00)  # exactly 50 is not > 50
        self.assertAlmostEqual(shipping_cost(31, "US", False, True), 46.35)  # 51.50 * 0.9
        self.assertAlmostEqual(shipping_cost(40, "CA", True, True), 92.70)  # 103 * 0.9

    def test_rounding(self):
        self.assertAlmostEqual(shipping_cost(1.333, "MX", False, False), 12.0)

    def test_bad_weight(self):
        for weight in (0, -1):
            with self.assertRaises(ValueError):
                shipping_cost(weight, "US", False, False)

    def test_bad_country(self):
        with self.assertRaises(ValueError) as ctx:
            shipping_cost(1, "FR", False, False)
        self.assertIn("FR", str(ctx.exception))

    def test_bad_weight_checked_before_country(self):
        with self.assertRaises(ValueError) as ctx:
            shipping_cost(0, "FR", False, False)
        self.assertIn("weight", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()

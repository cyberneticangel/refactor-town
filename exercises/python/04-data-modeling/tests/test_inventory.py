import unittest

from inventory import Inventory


def stocked():
    inv = Inventory()
    inv.add("widget", 2.50, 10)
    inv.add("gadget", 12.00, 3)
    inv.add("doohickey", 0.75, 100)
    inv.add("gizmo", 40.00, 1)
    return inv


class InventoryTests(unittest.TestCase):
    def test_total_value(self):
        self.assertAlmostEqual(stocked().total_value(), 25 + 36 + 75 + 40)

    def test_empty(self):
        inv = Inventory()
        self.assertEqual(inv.total_value(), 0)
        self.assertEqual(inv.low_stock(), [])
        self.assertIsNone(inv.most_valuable())

    def test_low_stock_keeps_insertion_order(self):
        self.assertEqual(stocked().low_stock(), ["gadget", "gizmo"])
        self.assertEqual(stocked().low_stock(threshold=11), ["widget", "gadget", "gizmo"])

    def test_restock(self):
        inv = stocked()
        inv.restock("gadget", 7)
        self.assertEqual(inv.low_stock(), ["gizmo"])
        self.assertAlmostEqual(inv.total_value(), 25 + 120 + 75 + 40)

    def test_restock_unknown(self):
        with self.assertRaises(KeyError):
            stocked().restock("sprocket", 1)

    def test_duplicate_add(self):
        inv = stocked()
        with self.assertRaises(ValueError):
            inv.add("widget", 1.0, 1)

    def test_most_valuable(self):
        inv = stocked()
        self.assertEqual(inv.most_valuable(), "doohickey")
        inv.restock("gizmo", 2)  # 120
        self.assertEqual(inv.most_valuable(), "gizmo")

    def test_most_valuable_tie_goes_to_first_added(self):
        inv = Inventory()
        inv.add("a", 1.0, 10)
        inv.add("b", 2.0, 5)
        self.assertEqual(inv.most_valuable(), "a")


if __name__ == "__main__":
    unittest.main()

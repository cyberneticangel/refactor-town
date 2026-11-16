import unittest

from stats import summarize


class SummarizeTests(unittest.TestCase):
    def test_typical_readings(self):
        self.assertEqual(
            summarize([12, 15, 9, 20]),
            {"count": 4, "total": 56, "average": 14.0, "highest": 20},
        )

    def test_negative_readings_are_ignored(self):
        result = summarize([10, -1, 30, -999, 20])
        self.assertEqual(result["count"], 3)
        self.assertEqual(result["total"], 60)
        self.assertEqual(result["average"], 20.0)
        self.assertEqual(result["highest"], 30)

    def test_zero_counts_as_valid(self):
        self.assertEqual(summarize([0, -5])["count"], 1)

    def test_no_valid_readings(self):
        expected = {"count": 0, "total": 0, "average": 0, "highest": None}
        self.assertEqual(summarize([]), expected)
        self.assertEqual(summarize([-3, -7]), expected)

    def test_floats(self):
        result = summarize([1.5, 2.5])
        self.assertAlmostEqual(result["average"], 2.0)
        self.assertEqual(result["highest"], 2.5)

    def test_input_is_not_modified(self):
        data = [5, -1, 7]
        summarize(data)
        self.assertEqual(data, [5, -1, 7])


if __name__ == "__main__":
    unittest.main()

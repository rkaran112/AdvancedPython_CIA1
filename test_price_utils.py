import unittest

import pandas as pd

from price_utils import filter_by_price_range


class TestFilterByPriceRange(unittest.TestCase):
    def setUp(self):
        self.df = pd.DataFrame({"Price_INR_per_kg": [10000, 20000, 25000, 30000, 40000]})

    def test_all_returns_every_row(self):
        result = filter_by_price_range(self.df, "All")
        self.assertEqual(list(result["Price_INR_per_kg"]), [10000, 20000, 25000, 30000, 40000])

    def test_less_than_or_equal_includes_boundary(self):
        result = filter_by_price_range(self.df, "Less than or equal to 20000")
        self.assertEqual(list(result["Price_INR_per_kg"]), [10000, 20000])

    def test_between_excludes_both_boundaries(self):
        result = filter_by_price_range(self.df, "Between 20000 and 30000")
        self.assertEqual(list(result["Price_INR_per_kg"]), [25000])

    def test_greater_than_or_equal_includes_boundary(self):
        result = filter_by_price_range(self.df, "Greater than or equal to 30000")
        self.assertEqual(list(result["Price_INR_per_kg"]), [30000, 40000])

    def test_boundaries_are_not_double_counted_across_filters(self):
        # Regression guard: every value must land in exactly one of the three
        # bounded bands, so a value like 20000 or 30000 is never counted twice.
        low = filter_by_price_range(self.df, "Less than or equal to 20000")
        mid = filter_by_price_range(self.df, "Between 20000 and 30000")
        high = filter_by_price_range(self.df, "Greater than or equal to 30000")
        self.assertEqual(len(low) + len(mid) + len(high), len(self.df))

    def test_unknown_filter_returns_df_unfiltered(self):
        result = filter_by_price_range(self.df, "not a real option")
        self.assertEqual(len(result), len(self.df))


if __name__ == "__main__":
    unittest.main()

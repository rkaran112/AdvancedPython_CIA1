import unittest

import pandas as pd

from price_utils import filter_by_price_range, parse_historical_prices


class TestParseHistoricalPrices(unittest.TestCase):
    def test_builds_date_from_year_and_month(self):
        hist_raw = pd.DataFrame({
            "Year": [2000, 2000, 2001],
            "Month": ["Jan", "Feb", "Jan"],
            "Silver_Price_INR_per_kg": [8030, 8075, 8500],
        })
        result = parse_historical_prices(hist_raw)
        self.assertEqual(
            list(result["Date"]),
            [pd.Timestamp("2000-01-01"), pd.Timestamp("2000-02-01"), pd.Timestamp("2001-01-01")],
        )
        self.assertEqual(list(result["Price_INR_per_kg"]), [8030, 8075, 8500])

    def test_output_has_only_date_and_price_columns(self):
        hist_raw = pd.DataFrame({
            "Year": [2000], "Month": ["Jan"], "Silver_Price_INR_per_kg": [8030],
        })
        result = parse_historical_prices(hist_raw)
        self.assertEqual(list(result.columns), ["Date", "Price_INR_per_kg"])


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

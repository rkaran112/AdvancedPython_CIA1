import unittest

import pandas as pd

from trend_utils import growth_percent, weekly_breakdown


class TestWeeklyBreakdown(unittest.TestCase):
    def test_buckets_days_into_four_weeks(self):
        df = pd.DataFrame({"Day": range(1, 32), "Silver_Purchased_kg": [10] * 31})
        result = weekly_breakdown(df)
        self.assertEqual(
            list(result["Week"]),
            ["Week 1 (1-7)", "Week 2 (8-14)", "Week 3 (15-21)", "Week 4 (22-31)"],
        )
        self.assertEqual(list(result["Total (kg)"]), [70, 70, 70, 100])

    def test_short_month_labels_last_week_by_actual_end_day(self):
        df = pd.DataFrame({"Day": range(1, 29), "Silver_Purchased_kg": [1] * 28})
        result = weekly_breakdown(df)
        self.assertEqual(result["Week"].iloc[-1], "Week 4 (22-28)")


class TestGrowthPercent(unittest.TestCase):
    def test_computes_percent_change(self):
        self.assertAlmostEqual(growth_percent(100, 150), 50.0)

    def test_returns_none_when_start_is_zero(self):
        self.assertIsNone(growth_percent(0, 50))


if __name__ == "__main__":
    unittest.main()

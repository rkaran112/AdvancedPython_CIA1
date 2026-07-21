import unittest

import pandas as pd

from state_utils import STATE_NAME_MAP, normalize_state_names, summarize_purchases


class TestNormalizeStateNames(unittest.TestCase):
    def test_known_variants_map_to_canonical_name(self):
        result = normalize_state_names(["Chattisgarh", "Orissa", "Pondicherry"])
        self.assertEqual(list(result), ["Chhattisgarh", "Odisha", "Puducherry"])

    def test_chattisgarh_maps_forward_not_reversed(self):
        # Regression guard: the map must go misspelling -> canonical, not the
        # reverse, so the canonical "Chhattisgarh" name must never be rewritten.
        self.assertEqual(normalize_state_names(["Chhattisgarh"])[0], "Chhattisgarh")

    def test_unmapped_names_are_left_unchanged(self):
        result = normalize_state_names(["Karnataka", "Tamil Nadu"])
        self.assertEqual(list(result), ["Karnataka", "Tamil Nadu"])

    def test_whitespace_is_stripped_before_mapping(self):
        result = normalize_state_names([" Orissa ", "  Karnataka"])
        self.assertEqual(list(result), ["Odisha", "Karnataka"])

    def test_mapping_values_are_not_themselves_keys(self):
        # Guards against accidental double-mapping / cyclic entries.
        for canonical in STATE_NAME_MAP.values():
            self.assertNotIn(canonical, STATE_NAME_MAP)

    def test_returns_a_series(self):
        result = normalize_state_names(pd.Series(["Orissa"]))
        self.assertIsInstance(result, pd.Series)


class TestSummarizePurchases(unittest.TestCase):
    def setUp(self):
        self.df = pd.DataFrame({
            "State": ["Rajasthan", "Gujarat", "Bihar"],
            "Silver_Purchased_kg": [2500, 2200, 700],
        })

    def test_computes_total_and_average(self):
        summary = summarize_purchases(self.df)
        self.assertEqual(summary["total"], 5400)
        self.assertAlmostEqual(summary["average"], 1800)

    def test_identifies_top_and_bottom_states(self):
        summary = summarize_purchases(self.df)
        self.assertEqual(summary["top_name"], "Rajasthan")
        self.assertEqual(summary["top_value"], 2500)
        self.assertEqual(summary["bottom_name"], "Bihar")
        self.assertEqual(summary["bottom_value"], 700)

    def test_computes_difference_between_top_and_bottom(self):
        summary = summarize_purchases(self.df)
        self.assertEqual(summary["difference"], 1800)

    def test_single_row_has_zero_difference(self):
        summary = summarize_purchases(pd.DataFrame({"State": ["Goa"], "Silver_Purchased_kg": [1600]}))
        self.assertEqual(summary["top_name"], summary["bottom_name"])
        self.assertEqual(summary["difference"], 0)


if __name__ == "__main__":
    unittest.main()

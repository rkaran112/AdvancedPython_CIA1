import unittest

import pandas as pd

from state_utils import STATE_NAME_MAP, normalize_state_names


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


if __name__ == "__main__":
    unittest.main()

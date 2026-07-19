import unittest

from calculator_utils import CURRENCY_RATES, convert_currency, weight_to_grams


class TestWeightToGrams(unittest.TestCase):
    def test_kilograms_are_converted_to_grams(self):
        self.assertEqual(weight_to_grams(2.5, "kilograms"), 2500)

    def test_grams_are_returned_unchanged(self):
        self.assertEqual(weight_to_grams(150, "grams"), 150)


class TestConvertCurrency(unittest.TestCase):
    def test_inr_is_unchanged(self):
        self.assertEqual(convert_currency(1000, "INR"), 1000)

    def test_applies_known_currency_rate(self):
        self.assertAlmostEqual(convert_currency(1000, "USD"), 1000 * CURRENCY_RATES["USD"])

    def test_unknown_currency_defaults_to_one_to_one(self):
        self.assertEqual(convert_currency(1000, "XYZ"), 1000)


if __name__ == "__main__":
    unittest.main()

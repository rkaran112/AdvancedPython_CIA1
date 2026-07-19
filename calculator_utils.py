"""Shared helpers for the Price Calculator tab's weight/currency conversion."""

CURRENCY_RATES = {
    "INR": 1.0,
    "USD": 0.012,
    "EUR": 0.011,
    "GBP": 0.0095,
    "AUD": 0.018,
}


def weight_to_grams(weight, unit):
    """Convert `weight` to grams, given unit "grams" or "kilograms"."""
    return weight * 1000 if unit == "kilograms" else weight


def convert_currency(amount_inr, currency, rates=CURRENCY_RATES):
    """Convert an INR amount to `currency` using `rates`, defaulting to 1:1 for unknown currencies."""
    return amount_inr * rates.get(currency, 1.0)

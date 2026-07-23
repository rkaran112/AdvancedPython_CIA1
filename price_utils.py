"""Shared helpers for the Historical Prices tab's CSV parsing and price-range filter."""

import pandas as pd

PRICE_FILTER_OPTIONS = [
    "All",
    "Less than or equal to 20000",
    "Between 20000 and 30000",
    "Greater than or equal to 30000",
]


def parse_historical_prices(hist_raw, year_col="Year", month_col="Month", price_col="Silver_Price_INR_per_kg"):
    """Build a Date/Price_INR_per_kg DataFrame from the raw historical-price CSV columns."""
    return pd.DataFrame({
        "Date": pd.to_datetime(hist_raw[year_col].astype(str) + "-" + hist_raw[month_col], format="%Y-%b"),
        "Price_INR_per_kg": hist_raw[price_col],
    })


def filter_by_price_range(df, price_filter, col="Price_INR_per_kg"):
    """Return the rows of `df` whose `col` value falls in the selected price band.

    The three bounded options partition the value line with no gaps and no
    overlap (<=20000, then >20000 and <30000, then >=30000), so every finite
    value matches exactly one of them. Any other `price_filter` value
    (including "All") returns `df` unfiltered.
    """
    if price_filter == "Less than or equal to 20000":
        return df[df[col] <= 20000]
    if price_filter == "Between 20000 and 30000":
        return df[(df[col] > 20000) & (df[col] < 30000)]
    if price_filter == "Greater than or equal to 30000":
        return df[df[col] >= 30000]
    return df

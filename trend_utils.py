"""Shared helpers for the January Trends tab's weekly breakdown and growth stats."""

import pandas as pd


def weekly_breakdown(df, day_col="Day", value_col="Silver_Purchased_kg"):
    """Bucket daily purchase data into weekly totals (days 1-7, 8-14, 15-21, 22-end).

    Returns a DataFrame with "Week" and "Total (kg)" columns, in week order.
    """
    last_day = int(df[day_col].max())
    bins = [0, 7, 14, 21, last_day]
    labels = [
        "Week 1 (1-7)",
        "Week 2 (8-14)",
        "Week 3 (15-21)",
        f"Week 4 (22-{last_day})",
    ]
    week = pd.cut(df[day_col], bins=bins, labels=labels)
    totals = df.groupby(week, observed=True)[value_col].sum()
    return pd.DataFrame({"Week": totals.index.astype(str), "Total (kg)": totals.values})


def growth_percent(start, end):
    """Percent change from `start` to `end`, or None if `start` is 0 (avoids a division by zero)."""
    if start == 0:
        return None
    return (end - start) / start * 100

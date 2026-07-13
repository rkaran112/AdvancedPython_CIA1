"""Shared state-name normalization used when merging the sales CSV with a GeoJSON."""

import pandas as pd

# Maps common alternate/legacy spellings of Indian state & UT names (as they
# appear in various GeoJSON sources) to the canonical spelling used in
# state_wise_silver_purchased_kg.csv.
STATE_NAME_MAP = {
    'Andaman & Nicobar': 'Andaman and Nicobar Islands',
    'A & N Islands': 'Andaman and Nicobar Islands',
    'Arunanchal Pradesh': 'Arunachal Pradesh',
    'Chattisgarh': 'Chhattisgarh',
    'Dadara & Nagar Haveli': 'Dadra and Nagar Haveli',
    'Daman & Diu': 'Daman and Diu',
    'NCT of Delhi': 'Delhi',
    'Jammu & Kashmir': 'Jammu and Kashmir',
    'Pondicherry': 'Puducherry',
    'Uttaranchal': 'Uttarakhand',
    'Orissa': 'Odisha',
}


def normalize_state_names(names, mapping=STATE_NAME_MAP):
    """Strip whitespace and apply STATE_NAME_MAP to a column of state names."""
    return pd.Series(names).astype(str).str.strip().replace(mapping)

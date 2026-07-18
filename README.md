# AdvancedPython_CIA1

CIA1 coursework for an Advanced Python course (3MCA-B): a Streamlit silver-price/sales dashboard plus a Jupyter notebook covering data-cleaning and EDA labs.

## What's in this repo

This repo bundles two separate pieces of coursework:

### 1. Silver Price Dashboard (`streamlit.py`)

A multi-tab Streamlit app ("Silver Price Calculator & Sales Dashboard", by R. Karan, RegNo 2547241, Class 3MCA-B) with four tabs:

- **Price Calculator** — interactive sliders/inputs to compute the cost of a silver purchase in grams or kilograms, converted to INR/USD/EUR/GBP/AUD at hard-coded exchange rates.
- **Historical Prices** — a line chart of silver price trends with a price-range filter and summary stats, sourced from `historical_silver_price.csv` (monthly INR/kg prices from 2000-2025), falling back to a synthetic series if the file is missing.
- **State-wise Sales** — loads `state_wise_silver_purchased_kg.csv` (falls back to a small hard-coded dataset if the file is missing) and shows a sortable/searchable table, a top-5 bar chart, and an optional India choropleth map. The map auto-loads the bundled `india_state_geo.json`, with an optional file uploader to override it with a different GeoJSON, and includes state-name normalization logic plus error handling for mismatched/invalid uploads.
- **January Trends** — a hard-coded daily dataset for January with a line chart, cumulative-purchases area chart, and weekly breakdown/growth stats.

### 2. `ML_2547241_Lab1&2.ipynb`

A Google Colab notebook (Lab 1 & Lab 2) doing data cleaning and exploratory analysis on two datasets — `city_day.csv` (air quality) and `crop_production.csv` — that are **not included in this repo** and are expected at `/content/...` (Colab's local storage). It walks through:

- Initial data profiling (shape, dtypes, missing values, describe)
- Missing-value treatment (column drops, median/mode imputation) with written justification
- State-name harmonization between the two datasets and duplicate removal
- AQI distribution analysis (histograms, per-city bar plots) and outlier handling via IQR-based winsorization
- Yearly and monthly AQI trend analysis, with written responses to a "journalist" and an "NGO" prompt
- Merging the two datasets at the state level and a correlation analysis (AQI vs. crop production/area)
- A closing summary letter addressed to a "Minister" synthesizing the findings

The notebook cannot be re-run outside Colab as-is, since it reads from `/content/` paths that don't exist locally.

## Tech stack

- Python
- **Dashboard:** Streamlit, pandas, Altair, GeoPandas (optional — the app degrades gracefully if it's not installed), Matplotlib, Fiona, pyproj, Shapely
- **Notebook:** pandas, matplotlib, seaborn (run in Google Colab)

## Setup

```bash
pip install -r requirements.txt
```

`requirements.txt` lists: `streamlit`, `pandas`, `altair`, `geopandas`, `matplotlib`, `fiona`, `pyproj`, `shapely`.

## Usage

```bash
streamlit run streamlit.py
```

Run this from the repo root so it can find `state_wise_silver_purchased_kg.csv` and `india_state_geo.json` — the choropleth map in the "State-wise Sales" tab loads the bundled `india_state_geo.json` automatically, or you can upload a different GeoJSON via the file uploader in that tab.

The notebook (`ML_2547241_Lab1&2.ipynb`) is designed for Google Colab and expects `city_day.csv` and `crop_production.csv` to be uploaded to `/content/` — those source datasets are not included in this repo.

## Status

Work in progress / rough edges, though functionally usable:

- `streamlit.py` runs end-to-end and has basic error handling (missing-CSV fallback, try/except around GeoPandas import and map generation). `historical_silver_price.csv` is wired up in the "Historical Prices" tab, and `india_state_geo.json` now auto-loads in the "State-wise Sales" map tab instead of requiring a manual upload.
- The notebook depends on external datasets (`city_day.csv`, `crop_production.csv`) that aren't included in the repo, so it can't be re-executed as-is outside the original Colab session.
- `test_state_utils.py` covers the state-name normalization helper, `test_trend_utils.py` covers the January Trends weekly breakdown/growth calculation, and `test_price_utils.py` covers the Historical Prices tab's price-range filter (`unittest`, run with `python -m unittest discover`). The rest of `streamlit.py` still has no automated tests.

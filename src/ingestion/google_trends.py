"""
MEPS Google Trends ingestion.

Purpose:
    Ingest country-level Google Trends search interest for the
    crypto-demand signal used by MEPS.

Methodology:
    A single worldwide Google Trends request is used so that the
    target countries share the same normalization framework.

Target countries:
    Ghana, Kenya, Nigeria, South Africa

Indicator:
    crypto_search_interest

Period:
    2025
"""

from pathlib import Path

import pandas as pd
from pytrends.request import TrendReq


# -------------------------------------------------------------------
# Configuration
# -------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

OUTPUT_DIR = PROJECT_ROOT / "data" / "raw" / "google_trends"
OUTPUT_FILE = OUTPUT_DIR / "google_trends_crypto.csv"

SEARCH_TERM = "crypto"
TIMEFRAME = "2025-01-01 2025-12-31"

TARGET_COUNTRIES = {
    "Ghana": "GHA",
    "Kenya": "KEN",
    "Nigeria": "NGA",
    "South Africa": "ZAF",
}

EXPECTED_ROWS = len(TARGET_COUNTRIES)

INDICATOR = "crypto_search_interest"
SOURCE = "Google Trends"


# -------------------------------------------------------------------
# Retrieve Google Trends data
# -------------------------------------------------------------------

def retrieve_google_trends() -> pd.DataFrame:
    """Retrieve country-level search interest from one worldwide request."""

    print("Initializing Google Trends...")

    trends = TrendReq(
        hl="en-US",
        tz=180,
    )

    print(f"Query: {SEARCH_TERM}")
    print(f"Timeframe: {TIMEFRAME}")
    print("Geography: Worldwide")
    print("Resolution: Country")

    trends.build_payload(
        kw_list=[SEARCH_TERM],
        cat=0,
        timeframe=TIMEFRAME,
        geo="",
    )

    data = trends.interest_by_region(
        resolution="COUNTRY",
        inc_low_vol=True,
    )

    if data.empty:
        raise ValueError("Google Trends returned no data.")

    return data.reset_index()


# -------------------------------------------------------------------
# Prepare MEPS dataset
# -------------------------------------------------------------------

def prepare_dataset(data: pd.DataFrame) -> pd.DataFrame:
    """Filter target countries and standardize the MEPS schema."""

    required_columns = {"geoName", SEARCH_TERM}

    missing_columns = required_columns - set(data.columns)

    if missing_columns:
        raise ValueError(
            f"Missing expected Google Trends columns: {missing_columns}"
        )

    data = data[
        data["geoName"].isin(TARGET_COUNTRIES.keys())
    ].copy()

    if data.empty:
        raise ValueError(
            "None of the target MEPS countries were returned by Google Trends."
        )

    data["country_code"] = data["geoName"].map(TARGET_COUNTRIES)

    data["year"] = 2025

    data["indicator"] = INDICATOR

    data["value"] = pd.to_numeric(
        data[SEARCH_TERM],
        errors="coerce",
    )

    data["source"] = SOURCE

    output = data[
        [
            "country_code",
            "geoName",
            "year",
            "indicator",
            "value",
            "source",
        ]
    ].rename(
        columns={
            "geoName": "country",
        }
    )

    return output.sort_values("country_code").reset_index(drop=True)


# -------------------------------------------------------------------
# Data contract validation
# -------------------------------------------------------------------

def validate_data(data: pd.DataFrame) -> None:
    """Validate the MEPS Google Trends data contract."""

    print("\nRunning data contract validation...")

    required_columns = {
        "country_code",
        "country",
        "year",
        "indicator",
        "value",
        "source",
    }

    missing_columns = required_columns - set(data.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    # Expected number of records
    if len(data) != EXPECTED_ROWS:
        raise ValueError(
            f"Expected {EXPECTED_ROWS} rows, received {len(data)}."
        )

    # Countries
    expected_codes = set(TARGET_COUNTRIES.values())
    actual_codes = set(data["country_code"])

    if actual_codes != expected_codes:
        raise ValueError(
            f"Country mismatch. Expected {expected_codes}, "
            f"received {actual_codes}."
        )

    # Year
    if data["year"].nunique() != 1 or data["year"].iloc[0] != 2025:
        raise ValueError("Year validation failed.")

    # Indicator
    if data["indicator"].nunique() != 1:
        raise ValueError("Indicator validation failed.")

    if data["indicator"].iloc[0] != INDICATOR:
        raise ValueError("Unexpected indicator name.")

    # Numeric values
    if data["value"].isna().any():
        raise ValueError(
            "Google Trends contains missing values for target countries."
        )

    # Range
    if ((data["value"] < 0) | (data["value"] > 100)).any():
        raise ValueError(
            "Google Trends values must be between 0 and 100."
        )

    # Duplicate analytical grain
    duplicate_count = data.duplicated(
        subset=[
            "country_code",
            "indicator",
            "year",
        ]
    ).sum()

    if duplicate_count > 0:
        raise ValueError(
            f"Duplicate analytical grain records: {duplicate_count}"
        )

    # Country names
    expected_country_names = set(TARGET_COUNTRIES.keys())
    actual_country_names = set(data["country"])

    if actual_country_names != expected_country_names:
        raise ValueError("Country name validation failed.")

    print("DATA CONTRACT VALIDATION PASSED")


# -------------------------------------------------------------------
# Save dataset
# -------------------------------------------------------------------

def save_dataset(data: pd.DataFrame) -> None:
    """Save validated data to the MEPS raw-data directory."""

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    data.to_csv(
        OUTPUT_FILE,
        index=False,
    )

    print(f"\nSaved: {OUTPUT_FILE}")


# -------------------------------------------------------------------
# Main
# -------------------------------------------------------------------

def main() -> None:

    print("=" * 60)
    print("MEPS GOOGLE TRENDS INGESTION")
    print("=" * 60)

    raw_data = retrieve_google_trends()

    print(f"\nCountries returned by Google Trends: {len(raw_data)}")

    data = prepare_dataset(raw_data)

    print("\nPrepared dataset:")
    print(data.to_string(index=False))

    validate_data(data)

    print("\nValidation summary:")
    print(f"Rows: {len(data)}")
    print(f"Countries: {data['country_code'].nunique()}")
    print(f"Indicator: {data['indicator'].iloc[0]}")
    print(f"Year: {data['year'].iloc[0]}")
    print(f"Missing values: {data['value'].isna().sum()}")
    print(
        "Duplicate grain records:",
        data.duplicated(
            subset=["country_code", "indicator", "year"]
        ).sum(),
    )

    save_dataset(data)

    print("\nINGESTION SUCCESSFUL ✓")


if __name__ == "__main__":
    main()
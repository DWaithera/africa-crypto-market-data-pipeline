"""
MEPS Chainalysis ingestion.

Purpose:
    Validate the Chainalysis Global Crypto Adoption Index rank
    for the four MEPS target markets.

Source:
    Chainalysis 2024 Global Crypto Adoption Index

Important:
    The raw source value is a country rank.
    Rank direction is handled later during feature engineering.
    Ingestion does not convert rank into an artificial score.

Data contract:
    - Countries: GHA, KEN, NGA, ZAF
    - Year: 2024
    - Indicator: crypto_adoption_rank
    - Expected rows: 4
    - Missing values: 0
    - Grain: country_code + indicator + year
"""


from pathlib import Path

import pandas as pd


# -------------------------------------------------------------------
# Configuration
# -------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "chainalysis"
    / "chainalysis_crypto_adoption_2024.csv"
)

TARGET_COUNTRIES = {
    "GHA": "Ghana",
    "KEN": "Kenya",
    "NGA": "Nigeria",
    "ZAF": "South Africa",
}

EXPECTED_ROWS = 4

EXPECTED_YEAR = 2024

EXPECTED_INDICATOR = "crypto_adoption_rank"

EXPECTED_SOURCE = "Chainalysis"


# -------------------------------------------------------------------
# Load raw data
# -------------------------------------------------------------------

def load_data() -> pd.DataFrame:
    """
    Load the Chainalysis source extract.
    """

    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Chainalysis input file not found: {INPUT_FILE}"
        )

    df = pd.read_csv(INPUT_FILE)

    print(f"Loaded rows: {len(df)}")

    return df


# -------------------------------------------------------------------
# Data contract validation
# -------------------------------------------------------------------

def validate_data(df: pd.DataFrame) -> None:
    """
    Validate the Chainalysis MEPS data contract.
    """

    print("\nRunning data contract validation...")

    # ---------------------------------------------------------------
    # Required columns
    # ---------------------------------------------------------------

    required_columns = {
        "country_code",
        "country",
        "year",
        "indicator",
        "value",
        "source",
        "source_dataset",
    }

    missing_columns = required_columns - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    # ---------------------------------------------------------------
    # Expected record count
    # ---------------------------------------------------------------

    if len(df) != EXPECTED_ROWS:
        raise ValueError(
            f"Expected {EXPECTED_ROWS} rows, received {len(df)}."
        )

    # ---------------------------------------------------------------
    # Country codes
    # ---------------------------------------------------------------

    expected_codes = set(TARGET_COUNTRIES.keys())
    actual_codes = set(df["country_code"])

    if actual_codes != expected_codes:
        raise ValueError(
            f"Country mismatch. "
            f"Expected {expected_codes}, "
            f"received {actual_codes}."
        )

    # ---------------------------------------------------------------
    # Country names
    # ---------------------------------------------------------------

    expected_names = set(TARGET_COUNTRIES.values())
    actual_names = set(df["country"])

    if actual_names != expected_names:
        raise ValueError(
            f"Country name mismatch. "
            f"Expected {expected_names}, "
            f"received {actual_names}."
        )

    # ---------------------------------------------------------------
    # Year
    # ---------------------------------------------------------------

    if df["year"].nunique() != 1:
        raise ValueError(
            "Multiple years found in dataset."
        )

    if int(df["year"].iloc[0]) != EXPECTED_YEAR:
        raise ValueError(
            f"Expected year {EXPECTED_YEAR}, "
            f"received {df['year'].iloc[0]}."
        )

    # ---------------------------------------------------------------
    # Indicator
    # ---------------------------------------------------------------

    if df["indicator"].nunique() != 1:
        raise ValueError(
            "Multiple indicators found in dataset."
        )

    if df["indicator"].iloc[0] != EXPECTED_INDICATOR:
        raise ValueError(
            f"Unexpected indicator: "
            f"{df['indicator'].iloc[0]}"
        )

    # ---------------------------------------------------------------
    # Source
    # ---------------------------------------------------------------

    if df["source"].nunique() != 1:
        raise ValueError(
            "Multiple sources found in dataset."
        )

    if df["source"].iloc[0] != EXPECTED_SOURCE:
        raise ValueError(
            f"Unexpected source: "
            f"{df['source'].iloc[0]}"
        )

    # ---------------------------------------------------------------
    # Numeric values
    # ---------------------------------------------------------------

    values = pd.to_numeric(
        df["value"],
        errors="coerce",
    )

    if values.isna().any():
        raise ValueError(
            "Chainalysis contains missing or non-numeric "
            "rank values."
        )

    # ---------------------------------------------------------------
    # Rank validation
    # ---------------------------------------------------------------

    if (values <= 0).any():
        raise ValueError(
            "Chainalysis adoption ranks must be positive."
        )

    # ---------------------------------------------------------------
    # Duplicate analytical grain
    # ---------------------------------------------------------------

    duplicate_count = df.duplicated(
        subset=[
            "country_code",
            "indicator",
            "year",
        ]
    ).sum()

    if duplicate_count > 0:
        raise ValueError(
            f"Duplicate analytical grain records: "
            f"{duplicate_count}"
        )

    print("DATA CONTRACT VALIDATION PASSED")


# -------------------------------------------------------------------
# Main
# -------------------------------------------------------------------

def main() -> None:
    """
    Execute Chainalysis ingestion validation.
    """

    print("=" * 60)
    print("MEPS CHAINALYSIS CRYPTO ACTIVITY INGESTION")
    print("=" * 60)

    print(f"\nSource: {INPUT_FILE}")

    # ---------------------------------------------------------------
    # Load
    # ---------------------------------------------------------------

    df = load_data()

    # ---------------------------------------------------------------
    # Display raw dataset
    # ---------------------------------------------------------------

    print("\nRaw dataset:")

    print(
        df.to_string(index=False)
    )

    # ---------------------------------------------------------------
    # Validate
    # ---------------------------------------------------------------

    validate_data(df)

    # ---------------------------------------------------------------
    # Validation summary
    # ---------------------------------------------------------------

    print("\nValidation summary:")

    print(
        f"Rows: {len(df)}"
    )

    print(
        f"Countries: {df['country_code'].nunique()}"
    )

    print(
        f"Indicator: {df['indicator'].iloc[0]}"
    )

    print(
        f"Year: {df['year'].iloc[0]}"
    )

    print(
        f"Missing values: {df['value'].isna().sum()}"
    )

    duplicate_count = df.duplicated(
        subset=[
            "country_code",
            "indicator",
            "year",
        ]
    ).sum()

    print(
        f"Duplicate grain records: {duplicate_count}"
    )

    print(
        "\nINGESTION SUCCESSFUL ✓"
    )


# -------------------------------------------------------------------
# Script entry point
# -------------------------------------------------------------------

if __name__ == "__main__":
    main()
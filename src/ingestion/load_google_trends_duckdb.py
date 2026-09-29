"""
Load MEPS Google Trends data into DuckDB.

Source:
    data/raw/google_trends/google_trends_crypto.csv

Target:
    raw.raw_google_trends
"""

from pathlib import Path

import duckdb
import pandas as pd


# -------------------------------------------------------------------
# Configuration
# -------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

CSV_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "google_trends"
    / "google_trends_crypto.csv"
)

DUCKDB_FILE = PROJECT_ROOT / "dev.duckdb"

SCHEMA = "raw"
TABLE = "raw_google_trends"


# -------------------------------------------------------------------
# Load data
# -------------------------------------------------------------------

def load_data() -> pd.DataFrame:
    """Read the validated Google Trends CSV."""

    if not CSV_FILE.exists():
        raise FileNotFoundError(
            f"Google Trends CSV not found: {CSV_FILE}"
        )

    df = pd.read_csv(CSV_FILE)

    required_columns = {
        "country_code",
        "country",
        "year",
        "indicator",
        "value",
        "source",
    }

    missing_columns = required_columns - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    return df


# -------------------------------------------------------------------
# Validate before loading
# -------------------------------------------------------------------

def validate_data(df: pd.DataFrame) -> None:
    """Validate the dataset before loading into DuckDB."""

    if len(df) != 4:
        raise ValueError(
            f"Expected 4 rows, received {len(df)}."
        )

    expected_countries = {"GHA", "KEN", "NGA", "ZAF"}

    if set(df["country_code"]) != expected_countries:
        raise ValueError(
            "Unexpected country codes."
        )

    if df["value"].isna().any():
        raise ValueError(
            "Google Trends contains missing values."
        )

    if ((df["value"] < 0) | (df["value"] > 100)).any():
        raise ValueError(
            "Google Trends values must be between 0 and 100."
        )

    duplicate_count = df.duplicated(
        subset=[
            "country_code",
            "indicator",
            "year",
        ]
    ).sum()

    if duplicate_count > 0:
        raise ValueError(
            f"Duplicate grain records: {duplicate_count}"
        )


# -------------------------------------------------------------------
# DuckDB load
# -------------------------------------------------------------------

def load_to_duckdb(df: pd.DataFrame) -> None:
    """Load the dataset into the raw DuckDB schema."""

    con = duckdb.connect(str(DUCKDB_FILE))

    try:
        con.execute(f"CREATE SCHEMA IF NOT EXISTS {SCHEMA}")

        con.register("google_trends_df", df)

        con.execute(
            f"""
            CREATE OR REPLACE TABLE
            {SCHEMA}.{TABLE}
            AS
            SELECT *
            FROM google_trends_df
            """
        )

        result = con.execute(
            f"""
            SELECT
                COUNT(*) AS rows,
                COUNT(DISTINCT country_code) AS countries,
                COUNT(DISTINCT indicator) AS indicators,
                COUNT(*) - COUNT(value) AS missing_values
            FROM {SCHEMA}.{TABLE}
            """
        ).fetchone()

        duplicate_count = con.execute(
            f"""
            SELECT COUNT(*)
            FROM (
                SELECT
                    country_code,
                    indicator,
                    year,
                    COUNT(*) AS record_count
                FROM {SCHEMA}.{TABLE}
                GROUP BY
                    country_code,
                    indicator,
                    year
                HAVING COUNT(*) > 1
            )
            """
        ).fetchone()[0]

        print("\nDuckDB validation:")
        print(f"Rows: {result[0]}")
        print(f"Countries: {result[1]}")
        print(f"Indicators: {result[2]}")
        print(f"Missing values: {result[3]}")
        print(f"Duplicate grain records: {duplicate_count}")

        if result[0] != 4:
            raise ValueError("DuckDB row count validation failed.")

        if result[1] != 4:
            raise ValueError(
                "DuckDB country count validation failed."
            )

        if result[2] != 1:
            raise ValueError(
                "DuckDB indicator count validation failed."
            )

        if result[3] != 0:
            raise ValueError(
                "DuckDB missing-value validation failed."
            )

        if duplicate_count != 0:
            raise ValueError(
                "DuckDB duplicate-grain validation failed."
            )

    finally:
        con.close()


# -------------------------------------------------------------------
# Main
# -------------------------------------------------------------------

def main() -> None:

    print("=" * 60)
    print("MEPS GOOGLE TRENDS → DUCKDB")
    print("=" * 60)

    print(f"\nSource: {CSV_FILE}")
    print(f"Target: {SCHEMA}.{TABLE}")

    df = load_data()

    validate_data(df)

    load_to_duckdb(df)

    print("\nDUCKDB LOAD SUCCESSFUL ✓")


if __name__ == "__main__":
    main()
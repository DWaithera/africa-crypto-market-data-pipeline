"""
MEPS Chainalysis DuckDB loader.

Purpose:
    Load the validated Chainalysis Crypto Adoption Index
    raw extract into the MEPS DuckDB raw layer.

Input:
    data/raw/chainalysis/chainalysis_crypto_adoption_2024.csv

Output:
    raw.raw_chainalysis_crypto_adoption

Important:
    This loader preserves the raw Chainalysis rank.
    No normalization, scoring, or rank transformation
    occurs in the raw layer.
"""

from pathlib import Path

import duckdb
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

DUCKDB_FILE = PROJECT_ROOT / "dev.duckdb"

SCHEMA_NAME = "raw"

TABLE_NAME = "raw_chainalysis_crypto_adoption"


# -------------------------------------------------------------------
# Load CSV
# -------------------------------------------------------------------

def load_csv() -> pd.DataFrame:
    """
    Load the validated Chainalysis CSV.
    """

    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Chainalysis input file not found: {INPUT_FILE}"
        )

    df = pd.read_csv(INPUT_FILE)

    print(f"Loaded CSV rows: {len(df)}")

    return df


# -------------------------------------------------------------------
# Validate dataframe
# -------------------------------------------------------------------

def validate_dataframe(df: pd.DataFrame) -> None:
    """
    Validate the dataframe before loading it into DuckDB.
    """

    print("\nRunning DuckDB load validation...")

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

    if len(df) != 4:
        raise ValueError(
            f"Expected 4 rows, received {len(df)}."
        )

    if df["country_code"].nunique() != 4:
        raise ValueError(
            "Expected exactly 4 unique MEPS countries."
        )

    if df["indicator"].nunique() != 1:
        raise ValueError(
            "Expected exactly one indicator."
        )

    if df["indicator"].iloc[0] != "crypto_adoption_rank":
        raise ValueError(
            f"Unexpected indicator: {df['indicator'].iloc[0]}"
        )

    if df["year"].nunique() != 1:
        raise ValueError(
            "Expected exactly one reference year."
        )

    if int(df["year"].iloc[0]) != 2024:
        raise ValueError(
            f"Expected year 2024, received {df['year'].iloc[0]}."
        )

    values = pd.to_numeric(
        df["value"],
        errors="coerce",
    )

    if values.isna().any():
        raise ValueError(
            "Chainalysis rank contains missing or non-numeric values."
        )

    if (values <= 0).any():
        raise ValueError(
            "Chainalysis adoption ranks must be positive."
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
            f"Duplicate analytical grain records: {duplicate_count}"
        )

    print("DUCKDB LOAD VALIDATION PASSED")


# -------------------------------------------------------------------
# Load into DuckDB
# -------------------------------------------------------------------

def load_to_duckdb(df: pd.DataFrame) -> None:
    """
    Load the dataframe into the DuckDB raw schema.
    """

    print("\nConnecting to DuckDB...")

    con = duckdb.connect(str(DUCKDB_FILE))

    try:
        # -----------------------------------------------------------
        # Create raw schema
        # -----------------------------------------------------------

        con.execute(
            f"CREATE SCHEMA IF NOT EXISTS {SCHEMA_NAME}"
        )

        # -----------------------------------------------------------
        # Register dataframe
        # -----------------------------------------------------------

        con.register(
            "chainalysis_df",
            df,
        )

        # -----------------------------------------------------------
        # Replace raw table
        # -----------------------------------------------------------

        con.execute(
            f"""
            CREATE OR REPLACE TABLE
                {SCHEMA_NAME}.{TABLE_NAME}
            AS
                SELECT *
                FROM chainalysis_df
            """
        )

        # -----------------------------------------------------------
        # Verify loaded rows
        # -----------------------------------------------------------

        row_count = con.execute(
            f"""
            SELECT COUNT(*)
            FROM {SCHEMA_NAME}.{TABLE_NAME}
            """
        ).fetchone()[0]

        print(
            f"Rows loaded into "
            f"{SCHEMA_NAME}.{TABLE_NAME}: {row_count}"
        )

        if row_count != len(df):
            raise ValueError(
                f"DuckDB row count mismatch. "
                f"Expected {len(df)}, received {row_count}."
            )

        # -----------------------------------------------------------
        # Verify analytical grain
        # -----------------------------------------------------------

        duplicate_count = con.execute(
            f"""
            SELECT COUNT(*)
            FROM (
                SELECT
                    country_code,
                    indicator,
                    year,
                    COUNT(*) AS records
                FROM {SCHEMA_NAME}.{TABLE_NAME}
                GROUP BY
                    country_code,
                    indicator,
                    year
                HAVING COUNT(*) > 1
            )
            """
        ).fetchone()[0]

        if duplicate_count > 0:
            raise ValueError(
                f"DuckDB analytical grain contains "
                f"{duplicate_count} duplicate groups."
            )

        print("DuckDB analytical grain validation PASSED")

        # -----------------------------------------------------------
        # Display loaded data
        # -----------------------------------------------------------

        print("\nLoaded DuckDB table:")

        result = con.execute(
            f"""
            SELECT *
            FROM {SCHEMA_NAME}.{TABLE_NAME}
            ORDER BY country_code
            """
        ).fetchdf()

        print(
            result.to_string(index=False)
        )

    finally:
        con.close()

    print("\nDUCKDB LOAD SUCCESSFUL ✓")


# -------------------------------------------------------------------
# Main
# -------------------------------------------------------------------

def main() -> None:
    """
    Execute the Chainalysis DuckDB loading pipeline.
    """

    print("=" * 60)
    print("MEPS CHAINALYSIS → DUCKDB RAW LOADER")
    print("=" * 60)

    print(f"\nInput: {INPUT_FILE}")
    print(f"DuckDB: {DUCKDB_FILE}")
    print(
        f"Target: {SCHEMA_NAME}.{TABLE_NAME}"
    )

    # ---------------------------------------------------------------
    # Load CSV
    # ---------------------------------------------------------------

    df = load_csv()

    # ---------------------------------------------------------------
    # Validate dataframe
    # ---------------------------------------------------------------

    validate_dataframe(df)

    # ---------------------------------------------------------------
    # Load into DuckDB
    # ---------------------------------------------------------------

    load_to_duckdb(df)

    print("\nPIPELINE COMPLETED ✓")


# -------------------------------------------------------------------
# Script entry point
# -------------------------------------------------------------------

if __name__ == "__main__":
    main()
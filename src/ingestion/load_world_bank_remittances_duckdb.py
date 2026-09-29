import duckdb
import pandas as pd
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

CSV_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "world_bank_remittances"
    / "world_bank_remittances.csv"
)

DUCKDB_FILE = PROJECT_ROOT / "dev.duckdb"

print("=" * 60)
print("MEPS — LOAD WORLD BANK REMITTANCES INTO DUCKDB")
print("=" * 60)

print("\nReading validated CSV...")

df = pd.read_csv(CSV_FILE)

print(f"Rows loaded from CSV: {len(df)}")

print("\nConnecting to DuckDB...")

con = duckdb.connect(str(DUCKDB_FILE))

con.execute("""
    CREATE SCHEMA IF NOT EXISTS raw
""")

print("\nLoading data into raw.raw_world_bank_remittances...")

con.register(
    "world_bank_remittances_df",
    df
)

con.execute("""
    CREATE OR REPLACE TABLE
    raw.raw_world_bank_remittances AS

    SELECT *
    FROM world_bank_remittances_df
""")

row_count = con.execute("""
    SELECT COUNT(*)
    FROM raw.raw_world_bank_remittances
""").fetchone()[0]

country_count = con.execute("""
    SELECT COUNT(DISTINCT country_code)
    FROM raw.raw_world_bank_remittances
""").fetchone()[0]

indicator_count = con.execute("""
    SELECT COUNT(DISTINCT indicator_code)
    FROM raw.raw_world_bank_remittances
""").fetchone()[0]

missing_count = con.execute("""
    SELECT COUNT(*)
    FROM raw.raw_world_bank_remittances
    WHERE value IS NULL
""").fetchone()[0]

duplicate_count = con.execute("""
    SELECT COUNT(*)
    FROM (
        SELECT
            country_code,
            indicator_code,
            year,
            COUNT(*) AS records
        FROM raw.raw_world_bank_remittances
        GROUP BY
            country_code,
            indicator_code,
            year
        HAVING COUNT(*) > 1
    )
""").fetchone()[0]

print("\nRunning DuckDB validation...")

if row_count != 44:
    raise ValueError(
        f"Expected 44 rows, found {row_count}"
    )

if country_count != 4:
    raise ValueError(
        f"Expected 4 countries, found {country_count}"
    )

if indicator_count != 1:
    raise ValueError(
        f"Expected 1 indicator, found {indicator_count}"
    )

if missing_count != 1:
    raise ValueError(
        f"Expected 1 missing value, found {missing_count}"
    )

if duplicate_count != 0:
    raise ValueError(
        f"Duplicate grain records found: {duplicate_count}"
    )

print("\n" + "=" * 60)
print("DUCKDB LOAD SUCCESSFUL ✓")
print("=" * 60)

print(f"Database: {DUCKDB_FILE}")
print("Table: raw.raw_world_bank_remittances")
print(f"Rows: {row_count}")
print(f"Countries: {country_count}")
print(f"Indicators: {indicator_count}")
print(f"Missing values: {missing_count}")
print(f"Duplicate grain records: {duplicate_count}")

con.close()
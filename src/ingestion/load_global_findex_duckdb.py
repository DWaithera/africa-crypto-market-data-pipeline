import duckdb
import pandas as pd
from pathlib import Path


# ============================================================
# 1. PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

CSV_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "global_findex"
    / "global_findex_meps.csv"
)

DUCKDB_FILE = (
    PROJECT_ROOT
    / "dev.duckdb"
)


# ============================================================
# 2. LOAD CSV
# ============================================================

print("=" * 60)
print("MEPS — LOAD GLOBAL FINDEX DATA INTO DUCKDB")
print("=" * 60)

print("\nReading validated CSV...")

df = pd.read_csv(CSV_FILE)

print(f"Rows loaded from CSV: {len(df)}")


# ============================================================
# 3. CONNECT TO DUCKDB
# ============================================================

print("\nConnecting to DuckDB...")

con = duckdb.connect(str(DUCKDB_FILE))


# ============================================================
# 4. CREATE RAW SCHEMA
# ============================================================

con.execute("""
    CREATE SCHEMA IF NOT EXISTS raw
""")


# ============================================================
# 5. LOAD DATA INTO RAW TABLE
# ============================================================

print("\nLoading data into raw.raw_global_findex...")

con.register(
    "global_findex_df",
    df
)

con.execute("""
    CREATE OR REPLACE TABLE
    raw.raw_global_findex AS

    SELECT *
    FROM global_findex_df
""")


# ============================================================
# 6. VERIFY TABLE
# ============================================================

row_count = con.execute("""
    SELECT COUNT(*)
    FROM raw.raw_global_findex
""").fetchone()[0]

print(f"Rows in DuckDB: {row_count}")


# ============================================================
# 7. BASIC VALIDATION
# ============================================================

country_count = con.execute("""
    SELECT COUNT(DISTINCT country_code)
    FROM raw.raw_global_findex
""").fetchone()[0]

indicator_count = con.execute("""
    SELECT COUNT(DISTINCT indicator)
    FROM raw.raw_global_findex
""").fetchone()[0]

missing_count = con.execute("""
    SELECT COUNT(*)
    FROM raw.raw_global_findex
    WHERE value IS NULL
""").fetchone()[0]

duplicate_count = con.execute("""
    SELECT COUNT(*)
    FROM (
        SELECT
            country_code,
            indicator,
            year,
            COUNT(*) AS records
        FROM raw.raw_global_findex
        GROUP BY
            country_code,
            indicator,
            year
        HAVING COUNT(*) > 1
    )
""").fetchone()[0]


# ============================================================
# 8. FINAL VALIDATION
# ============================================================

print("\nRunning DuckDB validation...")

if row_count != 12:
    raise ValueError(
        f"Expected 12 rows, found {row_count}"
    )

if country_count != 4:
    raise ValueError(
        f"Expected 4 countries, found {country_count}"
    )

if indicator_count != 3:
    raise ValueError(
        f"Expected 3 indicators, found {indicator_count}"
    )

if missing_count != 0:
    raise ValueError(
        f"Expected 0 missing values, found {missing_count}"
    )

if duplicate_count != 0:
    raise ValueError(
        f"Duplicate grain records found: {duplicate_count}"
    )


# ============================================================
# 9. SUCCESS
# ============================================================

print("\n" + "=" * 60)
print("DUCKDB LOAD SUCCESSFUL ✓")
print("=" * 60)

print(f"Database: {DUCKDB_FILE}")
print("Table: raw.raw_global_findex")
print(f"Rows: {row_count}")
print(f"Countries: {country_count}")
print(f"Indicators: {indicator_count}")
print(f"Missing values: {missing_count}")
print(f"Duplicate grain records: {duplicate_count}")


# ============================================================
# 10. CLOSE CONNECTION
# ============================================================

con.close()
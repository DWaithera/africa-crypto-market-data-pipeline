from pathlib import Path
import pandas as pd


# =========================================================
# CONFIGURATION
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "global_findex"
    / "global_findex_2025.xlsx"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "global_findex"
    / "global_findex_meps.csv"
)

TARGET_COUNTRIES = {
    "Ghana": "GHA",
    "Kenya": "KEN",
    "Nigeria": "NGA",
    "South Africa": "ZAF",
}

TARGET_YEAR = "2024"

TARGET_INDICATORS = {
    "account.t.d": "account_ownership",
    "g20.any": "digital_payment_usage",
    "con9a": "smartphone_adoption",
}


# =========================================================
# LOAD DATA
# =========================================================

print("Loading Global Findex workbook...")

df = pd.read_excel(
    INPUT_FILE,
    sheet_name="Data",
    header=0
)

print(f"Raw shape: {df.shape}")


# =========================================================
# REMOVE DESCRIPTIVE HEADER ROW
# =========================================================

df = df[df["year"].astype(str).str.strip() != "Year"].copy()

df["year"] = df["year"].astype(str).str.strip()


# =========================================================
# FILTER MEPS POPULATION
# =========================================================

df = df[
    (df["year"] == TARGET_YEAR)
    & (df["group"].astype(str).str.lower() == "all")
    & (df["group2"].astype(str).str.lower() == "all")
    & (df["codewb"].isin(TARGET_COUNTRIES.values()))
].copy()


# =========================================================
# RESHAPE INDICATORS
# =========================================================

records = []

for series, indicator_name in TARGET_INDICATORS.items():

    temp = df[
        [
            "countrynewwb",
            "codewb",
            "year",
            series
        ]
    ].copy()

    temp = temp.rename(
        columns={
            "countrynewwb": "country",
            "codewb": "country_code",
            series: "value"
        }
    )

    temp["series"] = series
    temp["indicator"] = indicator_name

    records.append(temp)


output = pd.concat(
    records,
    ignore_index=True
)


# =========================================================
# SELECT FINAL COLUMNS
# =========================================================

output = output[
    [
        "country_code",
        "country",
        "year",
        "series",
        "indicator",
        "value"
    ]
].copy()


# =========================================================
# DATA TYPE CLEANING
# =========================================================

output["value"] = pd.to_numeric(
    output["value"],
    errors="coerce"
)


# =========================================================
# VALIDATION
# =========================================================

print("\nRunning data contract validation...")


# Countries
expected_countries = set(TARGET_COUNTRIES.values())
actual_countries = set(output["country_code"])

assert actual_countries == expected_countries, (
    f"Country mismatch. Expected {expected_countries}, "
    f"got {actual_countries}"
)


# Indicators
expected_indicators = set(TARGET_INDICATORS.values())
actual_indicators = set(output["indicator"])

assert actual_indicators == expected_indicators, (
    f"Indicator mismatch. Expected {expected_indicators}, "
    f"got {actual_indicators}"
)


# Expected records
expected_rows = 4 * 3

assert len(output) == expected_rows, (
    f"Expected {expected_rows} records, got {len(output)}"
)


# Year
assert output["year"].nunique() == 1
assert output["year"].iloc[0] == TARGET_YEAR


# Value range
invalid_values = output[
    output["value"].notna()
    & ~output["value"].between(0, 1)
]

assert len(invalid_values) == 0, (
    "Found values outside the valid proportion range 0–1"
)


# Duplicate grain
duplicates = output.duplicated(
    subset=[
        "country_code",
        "indicator",
        "year"
    ]
).sum()

assert duplicates == 0, (
    f"Duplicate grain records: {duplicates}"
)


# Missing values
missing_values = output["value"].isna().sum()


# =========================================================
# SOURCE METADATA
# =========================================================

output["source"] = "World Bank Global Findex 2025"


# =========================================================
# SAVE
# =========================================================

OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

output.to_csv(
    OUTPUT_FILE,
    index=False
)


# =========================================================
# FINAL REPORT
# =========================================================

print("\nGLOBAL FINDEX INGESTION SUCCESSFUL ✓")
print("-----------------------------------")
print(f"Rows: {len(output)}")
print(f"Countries: {output['country_code'].nunique()}")
print(f"Indicators: {output['indicator'].nunique()}")
print(f"Year: {TARGET_YEAR}")
print(f"Missing values: {missing_values}")
print(f"Duplicate grain records: {duplicates}")
print(f"Output: {OUTPUT_FILE}")
print("\nRecords by country:")
print(output.groupby("country_code").size())

print("\nRecords by indicator:")
print(output.groupby("indicator").size())
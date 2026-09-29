from pathlib import Path
import requests
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

OUTPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "world_bank"
    / "world_bank_remittances.csv"
)

API_URL = (
    "https://api.worldbank.org/v2/country/"
    "GHA;KEN;NGA;ZAF/indicator/"
    "BX.TRF.PWKR.DT.GD.ZS"
)

TARGET_COUNTRIES = {
    "GHA": "Ghana",
    "KEN": "Kenya",
    "NGA": "Nigeria",
    "ZAF": "South Africa",
}

INDICATOR_CODE = "BX.TRF.PWKR.DT.GD.ZS"
INDICATOR_NAME = "remittances_pct_gdp"

START_YEAR = 2015
END_YEAR = 2025

print("=" * 60)
print("MEPS — WORLD BANK REMITTANCES INGESTION")
print("=" * 60)

print("\nRequesting World Bank API data...")

response = requests.get(
    API_URL,
    params={
        "format": "json",
        "per_page": 1000,
    },
    timeout=30,
)

response.raise_for_status()

payload = response.json()

if not isinstance(payload, list) or len(payload) < 2:
    raise ValueError("Unexpected World Bank API response structure.")

metadata = payload[0]
records = payload[1]

if metadata.get("total") is None:
    raise ValueError("World Bank API metadata is missing total record count.")

print(f"API records received: {len(records)}")

rows = []

for record in records:
    country_code = record.get("countryiso3code")
    year = record.get("date")
    value = record.get("value")

    if country_code not in TARGET_COUNTRIES:
        continue

    try:
        year = int(year)
    except (TypeError, ValueError):
        continue

    if START_YEAR <= year <= END_YEAR:
        rows.append(
            {
                "country_code": country_code,
                "country": TARGET_COUNTRIES[country_code],
                "indicator_code": INDICATOR_CODE,
                "indicator_name": INDICATOR_NAME,
                "year": year,
                "value": value,
                "source": "World Bank World Development Indicators",
            }
        )

output = pd.DataFrame(rows)

print("\nRunning data contract validation...")

expected_countries = set(TARGET_COUNTRIES.keys())

actual_countries = set(output["country_code"])

assert actual_countries == expected_countries, (
    f"Country mismatch. Expected {expected_countries}, "
    f"got {actual_countries}"
)

assert output["indicator_code"].nunique() == 1
assert output["indicator_code"].iloc[0] == INDICATOR_CODE

assert output["indicator_name"].nunique() == 1
assert output["indicator_name"].iloc[0] == INDICATOR_NAME

assert output["year"].min() == START_YEAR
assert output["year"].max() == END_YEAR

expected_rows = 4 * 11

assert len(output) == expected_rows, (
    f"Expected {expected_rows} records, got {len(output)}"
)

output["value"] = pd.to_numeric(
    output["value"],
    errors="coerce"
)

invalid_values = output[
    output["value"].notna()
    & (output["value"] < 0)
]

assert len(invalid_values) == 0, (
    "Found negative remittance values."
)

duplicates = output.duplicated(
    subset=[
        "country_code",
        "indicator_code",
        "year",
    ]
).sum()

assert duplicates == 0, (
    f"Duplicate grain records found: {duplicates}"
)

missing_values = output["value"].isna().sum()

OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

output = output.sort_values(
    ["country_code", "year"]
).reset_index(drop=True)

output.to_csv(
    OUTPUT_FILE,
    index=False
)

print("\n" + "=" * 60)
print("WORLD BANK REMITTANCES INGESTION SUCCESSFUL ✓")
print("=" * 60)

print(f"Rows: {len(output)}")
print(f"Countries: {output['country_code'].nunique()}")
print(f"Indicator: {INDICATOR_NAME}")
print(f"Indicator code: {INDICATOR_CODE}")
print(f"Year range: {START_YEAR}–{END_YEAR}")
print(f"Missing values: {missing_values}")
print(f"Duplicate grain records: {duplicates}")
print(f"Output: {OUTPUT_FILE}")

print("\nRecords by country:")
print(output.groupby("country_code").size())

print("\nRemittance values:")
print(
    output[
        ["country_code", "year", "value"]
    ].to_string(index=False)
)
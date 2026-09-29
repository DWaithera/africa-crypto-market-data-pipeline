import requests
import pandas as pd
from pathlib import Path
from datetime import datetime, timezone


# ============================================================
# 1. DATA CONTRACT
# ============================================================

COUNTRIES = {
    "KEN": "Kenya",
    "NGA": "Nigeria",
    "GHA": "Ghana",
    "ZAF": "South Africa",
}

INDICATORS = {
    "SP.POP.TOTL": "population",
    "NY.GDP.PCAP.CD": "gdp_per_capita",
    "IT.NET.USER.ZS": "internet_penetration",
}

START_YEAR = 2015
END_YEAR = 2025

BASE_URL = "https://api.worldbank.org/v2"

OUTPUT_DIR = Path("data/raw/world_bank")
OUTPUT_FILE = OUTPUT_DIR / "world_bank_indicators.csv"


# ============================================================
# 2. FETCH WORLD BANK DATA
# ============================================================

def fetch_indicator(country_codes, indicator_code):
    """
    Fetch one World Bank indicator for the selected countries
    and requested period.
    """

    countries = ";".join(country_codes)

    url = (
        f"{BASE_URL}/country/{countries}/indicator/"
        f"{indicator_code}"
    )

    params = {
        "format": "json",
        "date": f"{START_YEAR}:{END_YEAR}",
        "per_page": 1000,
    }

    response = requests.get(
        url,
        params=params,
        timeout=30
    )

    response.raise_for_status()

    # Validate JSON response
    try:
        data = response.json()
    except ValueError as exc:
        raise ValueError(
            f"World Bank returned invalid JSON "
            f"for {indicator_code}"
        ) from exc

    # Validate overall response structure
    if not isinstance(data, list) or len(data) < 2:
        raise ValueError(
            f"Unexpected World Bank response structure "
            f"for {indicator_code}"
        )

    # Validate data payload
    if not isinstance(data[1], list):
        raise ValueError(
            f"World Bank data payload is not a list "
            f"for {indicator_code}"
        )

    # Make sure records were returned
    if len(data[1]) == 0:
        raise ValueError(
            f"No records returned for {indicator_code}"
        )

    return data[1]


# ============================================================
# 3. MAIN INGESTION PIPELINE
# ============================================================

def main():

    print("=" * 60)
    print("MEPS — WORLD BANK DATA INGESTION")
    print("=" * 60)

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    records = []

    # One extraction timestamp for the entire dataset
    extracted_at = datetime.now(
        timezone.utc
    ).isoformat()

    # --------------------------------------------------------
    # Fetch each indicator
    # --------------------------------------------------------

    for indicator_code, indicator_name in INDICATORS.items():

        print(
            f"\nFetching {indicator_name} "
            f"({indicator_code})..."
        )

        data = fetch_indicator(
            COUNTRIES.keys(),
            indicator_code
        )

        for row in data:

            records.append({
                "country_code": row.get(
                    "countryiso3code"
                ),

                "country": (
                    row.get("country", {}).get("value")
                    if isinstance(
                        row.get("country"),
                        dict
                    )
                    else None
                ),

                "indicator_code": indicator_code,

                "indicator_name": indicator_name,

                "year": int(row["date"]),

                "value": row["value"],

                "source": "World Bank",

                "extracted_at": extracted_at,
            })

    # --------------------------------------------------------
    # Create DataFrame
    # --------------------------------------------------------

    df = pd.DataFrame(records)

    print(
        f"\nRaw records retrieved: {len(df)}"
    )

    # --------------------------------------------------------
    # Keep only expected countries
    # --------------------------------------------------------

    df = df[
        df["country_code"].isin(
            COUNTRIES.keys()
        )
    ].copy()

    # ========================================================
    # 4. DATA CONTRACT VALIDATION
    # ========================================================

    print("\nRunning data contract validation...")

    # --------------------------------------------------------
    # Validate required columns
    # --------------------------------------------------------

    expected_columns = [
        "country_code",
        "country",
        "indicator_code",
        "indicator_name",
        "year",
        "value",
        "source",
        "extracted_at",
    ]

    missing_columns = (
        set(expected_columns)
        - set(df.columns)
    )

    if missing_columns:
        raise ValueError(
            f"Missing required columns: "
            f"{missing_columns}"
        )

    # --------------------------------------------------------
    # Validate countries
    # --------------------------------------------------------

    actual_countries = set(
        df["country_code"]
        .dropna()
        .unique()
    )

    expected_countries = set(
        COUNTRIES.keys()
    )

    if actual_countries != expected_countries:
        raise ValueError(
            f"Country mismatch.\n"
            f"Expected: {expected_countries}\n"
            f"Found: {actual_countries}"
        )

    # --------------------------------------------------------
    # Validate country names
    # --------------------------------------------------------

    for country_code, expected_name in COUNTRIES.items():

        actual_names = (
            df.loc[
                df["country_code"] == country_code,
                "country"
            ]
            .dropna()
            .unique()
        )

        if len(actual_names) != 1:
            raise ValueError(
                f"Unexpected country name mapping "
                f"for {country_code}: {actual_names}"
            )

        if actual_names[0] != expected_name:
            raise ValueError(
                f"Country name mismatch for "
                f"{country_code}.\n"
                f"Expected: {expected_name}\n"
                f"Found: {actual_names[0]}"
            )

    # --------------------------------------------------------
    # Validate indicators
    # --------------------------------------------------------

    actual_indicators = set(
        df["indicator_code"]
        .dropna()
        .unique()
    )

    expected_indicators = set(
        INDICATORS.keys()
    )

    if actual_indicators != expected_indicators:
        raise ValueError(
            f"Indicator mismatch.\n"
            f"Expected: {expected_indicators}\n"
            f"Found: {actual_indicators}"
        )

    # --------------------------------------------------------
    # Validate years
    # --------------------------------------------------------

    if df["year"].isna().any():
        raise ValueError(
            "Missing year values detected."
        )

    if not pd.api.types.is_integer_dtype(
        df["year"]
    ):
        raise ValueError(
            "Year column must be integer."
        )

    if not df["year"].between(
        START_YEAR,
        END_YEAR
    ).all():
        raise ValueError(
            f"Year outside expected range "
            f"{START_YEAR}–{END_YEAR}"
        )

    # --------------------------------------------------------
    # Validate numeric values
    # --------------------------------------------------------

    if not pd.api.types.is_numeric_dtype(
        df["value"]
    ):
        raise ValueError(
            "Value column must be numeric."
        )

    # --------------------------------------------------------
    # Validate population and GDP
    # --------------------------------------------------------

    for indicator in [
        "SP.POP.TOTL",
        "NY.GDP.PCAP.CD"
    ]:

        invalid_values = df[
            (df["indicator_code"] == indicator)
            & (df["value"].notna())
            & (df["value"] < 0)
        ]

        if not invalid_values.empty:
            raise ValueError(
                f"Negative values detected "
                f"for {indicator}."
            )

    # --------------------------------------------------------
    # Validate internet penetration
    # --------------------------------------------------------

    internet_values = df[
        (df["indicator_code"] == "IT.NET.USER.ZS")
        & (df["value"].notna())
    ]

    if not internet_values["value"].between(
        0,
        100
    ).all():

        raise ValueError(
            "Internet penetration contains "
            "values outside 0–100."
        )

    # --------------------------------------------------------
    # Report missing values
    # --------------------------------------------------------

    missing_values = df[
        df["value"].isna()
    ]

    print(
        f"\nMissing indicator values: "
        f"{len(missing_values)}"
    )

    if not missing_values.empty:

        print("\nMissing observations:")

        print(
            missing_values[
                [
                    "country_code",
                    "indicator_code",
                    "year"
                ]
            ].to_string(index=False)
        )

    # --------------------------------------------------------
    # Validate grain / duplicates
    # --------------------------------------------------------

    grain_columns = [
        "country_code",
        "indicator_code",
        "year"
    ]

    duplicate_rows = df.duplicated(
        subset=grain_columns,
        keep=False
    )

    if duplicate_rows.any():

        print("\nDuplicate records:")

        print(
            df.loc[
                duplicate_rows,
                grain_columns
            ].to_string(index=False)
        )

        raise ValueError(
            "Duplicate records detected "
            "at expected grain."
        )

    # --------------------------------------------------------
    # Validate expected row count
    # --------------------------------------------------------

    expected_rows = (
        len(COUNTRIES)
        * len(INDICATORS)
        * (END_YEAR - START_YEAR + 1)
    )

    actual_rows = len(df)

    if actual_rows != expected_rows:
        raise ValueError(
            f"Unexpected row count.\n"
            f"Expected: {expected_rows}\n"
            f"Found: {actual_rows}"
        )

    # --------------------------------------------------------
    # Validate source
    # --------------------------------------------------------

    if df["source"].isna().any():
        raise ValueError(
            "Missing source values detected."
        )

    if not (
        df["source"] == "World Bank"
    ).all():

        raise ValueError(
            "Unexpected source value detected."
        )

    # ========================================================
    # 5. SORT DATA
    # ========================================================

    df = df.sort_values(
        [
            "country_code",
            "indicator_code",
            "year"
        ]
    ).reset_index(drop=True)

    # ========================================================
    # 6. SAVE VALIDATED DATA
    # ========================================================

    df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    # ========================================================
    # 7. FINAL SUMMARY
    # ========================================================

    print("\n" + "=" * 60)
    print("DATA CONTRACT VALIDATION PASSED")
    print("=" * 60)

    print(
        f"Output: {OUTPUT_FILE}"
    )

    print(
        f"Rows: {len(df)}"
    )

    print(
        f"Columns: {len(df.columns)}"
    )

    print(
        f"Countries: {df['country'].nunique()}"
    )

    print(
        f"Indicators: "
        f"{df['indicator_code'].nunique()}"
    )

    print(
        f"Year range: "
        f"{df['year'].min()}–"
        f"{df['year'].max()}"
    )

    print(
        f"Missing values: "
        f"{df['value'].isna().sum()}"
    )

    print(
        f"Duplicate grain records: "
        f"{df.duplicated(subset=grain_columns).sum()}"
    )

    print("\nINGESTION SUCCESSFUL ✓")


# ============================================================
# 8. SCRIPT ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()
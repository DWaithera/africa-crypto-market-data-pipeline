Africa Crypto Market Data Pipeline
A data pipeline for collecting, validating, and preparing public crypto-market data across four African markets for business analysis.
---
Overview
This project brings together public data from multiple sources to create a consistent data foundation for analysing:
Ghana · Kenya · Nigeria · South Africa
The data covers crypto adoption, crypto interest, financial access, digital payments, internet access, economic indicators, and remittances.
---
Business Problem
Information about emerging markets is often spread across different sources, formats, and reporting periods.
Before comparing markets, the data needs to be collected, checked, and standardized.
This project focuses on that foundation:
Collect → Validate → Standardize → Prepare for Analysis
---
What I Built
The pipeline collects public datasets, preserves the raw data, loads it into DuckDB, and uses dbt to standardize and validate the data.
```text
Public Data Sources
        ↓
Python
        ↓
Raw Data
        ↓
DuckDB
        ↓
dbt
        ↓
Validated Data
        ↓
Business Analysis
```
Data Sources
Source	Data
World Bank	Population, GDP per capita, internet access, remittances
Global Findex	Financial access, digital payments, smartphone adoption
Google Trends	Crypto search interest
Chainalysis	Crypto adoption
Markets
Country	Code
Ghana	GHA
Kenya	KEN
Nigeria	NGA
South Africa	ZAF
---
Business Value
The project creates a reliable starting point for comparing African crypto markets.
It brings information from different sources into a consistent structure so analysts can investigate:
Market environment
Financial access
Digital readiness
Crypto interest and adoption
Economic context
The focus is on getting the data foundation right before using it for business analysis.
---
Data Quality
The pipeline validates data during ingestion and transformation.
Validation includes:
Required fields
Country and indicator values
Data types
Analytical grain
Missing observations
35 / 35 dbt tests passed.
---
Technology
Python · Pandas · DuckDB · SQL · dbt · Git · GitHub
---
Repository
```text
data/
└── raw/

src/
└── ingestion/

dbt/
├── models/
│   ├── sources/
│   └── staging/
└── tests/

docs/
```
---
Author
Damaris Waithera
Data Analyst | FinTech & Web3 | Emerging Markets
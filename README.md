\# 🌍 Africa Crypto Market Data Pipeline



> \*\*A data pipeline for collecting, validating, and preparing public crypto-market data across four African markets for business analysis.\*\*



\[!\[Python](https://img.shields.io/badge/Python-Data%20Ingestion-blue)]()

\[!\[DuckDB](https://img.shields.io/badge/DuckDB-Data%20Storage-orange)]()

\[!\[dbt](https://img.shields.io/badge/dbt-Data%20Quality-red)]()

\[!\[GitHub](https://img.shields.io/badge/GitHub-Version%20Control-black)]()



\---



\## 🎯 Project Purpose



Understanding an emerging market requires more than finding individual numbers.



Public information about African crypto markets is spread across different sources, formats, definitions, and reporting periods.



This project brings that information together for:



🇬🇭 \*\*Ghana\*\* · 🇰🇪 \*\*Kenya\*\* · 🇳🇬 \*\*Nigeria\*\* · 🇿🇦 \*\*South Africa\*\*



The goal is to create a \*\*reliable data foundation\*\* that can be used to understand differences between markets and support future business analysis.



\### The business problem



A business evaluating an emerging market may need to understand:



\- How digitally connected is the market?

\- How accessible are financial services?

\- How widely are digital payments used?

\- What signals exist around crypto interest and adoption?

\- How does the broader economic environment differ between markets?



Answering these questions requires information from multiple sources.



The challenge is making that information \*\*consistent, traceable, and trustworthy before using it to make comparisons.\*\*



\---



\## 💡 Business Value



This project turns:



\*\*Fragmented public information\*\*



↓



\*\*Validated and standardized data\*\*



↓



\*\*Analysis-ready information\*\*



↓



\*\*Better business questions\*\*



The pipeline does not make the final market decision.



Instead, it creates the data foundation needed to investigate questions such as:



> \*\*How do these markets differ?\*\*



> \*\*What signals should a business investigate further?\*\*



> \*\*Is the available information reliable enough to support a decision?\*\*



\---



\## 🏗️ What I Built



```text

&#x20;                 PUBLIC DATA SOURCES

&#x20;                         │

&#x20;                         ▼

&#x20;                 Python Ingestion

&#x20;                         │

&#x20;                         ▼

&#x20;                    Raw Data

&#x20;                         │

&#x20;                         ▼

&#x20;                      DuckDB

&#x20;                         │

&#x20;                         ▼

&#x20;                   dbt Staging

&#x20;                         │

&#x20;               ┌─────────┴─────────┐

&#x20;               ▼                   ▼

&#x20;          Validation          Standardization

&#x20;               │                   │

&#x20;               └─────────┬─────────┘

&#x20;                         ▼

&#x20;                ANALYSIS-READY DATA

&#x20;                         │

&#x20;                         ▼

&#x20;                 BUSINESS ANALYSIS

1\. Collect



Public datasets are collected from multiple sources and preserved in their raw form.



2\. Validate



The incoming data is checked for issues such as:



Missing required fields

Invalid country codes

Invalid indicator values

Unexpected data types

Duplicate analytical records

3\. Standardize



Different sources are brought into consistent analytical structures so they can be queried and compared more easily.



4\. Prepare



The final staging datasets provide a clean foundation for downstream analysis.



🌍 Data Sources

Source	Business Context

World Bank	Population, GDP per capita, internet access

Global Findex	Account ownership, digital payments, smartphone adoption

Google Trends	Crypto-related search interest

Chainalysis	Crypto adoption ranking

World Bank Remittances	Remittance flows relative to GDP

Markets covered

Market	Country Code

🇬🇭 Ghana	GHA

🇰🇪 Kenya	KEN

🇳🇬 Nigeria	NGA

🇿🇦 South Africa	ZAF

📊 What the Data Can Help Answer



The pipeline creates a foundation for questions around:



Market Environment



How different are the four markets in terms of population, economic activity and digital connectivity?



Financial Access



How does access to formal financial services differ between markets?



Digital Readiness



What does internet access, smartphone adoption and digital-payment usage look like across countries?



Crypto Interest \& Adoption



Where do we see stronger signals of crypto interest or reported adoption?



Market Context



How do remittance flows and broader economic indicators differ between markets?



These are analytical questions, not conclusions produced by this repository.



🔍 Data Quality



Data quality is treated as part of the analysis process.



Python + DuckDB



The ingestion layer checks the incoming data and validates the expected analytical grain before loading it into the database.



dbt



The staging layer applies tests for required fields and expected values.



Current QA result

35 tests passed

0 warnings

0 errors



The pipeline also preserves expected source-level missing values rather than silently replacing them.



A missing value should be understood before it is changed.



🧱 Data Model



The project separates the data into two simple layers.



Raw Layer



Preserves source data for traceability.



raw.raw\_world\_bank\_indicators

raw.raw\_global\_findex

raw.raw\_google\_trends

raw.raw\_chainalysis\_crypto\_adoption

raw.raw\_world\_bank\_remittances

Staging Layer



Creates standardized datasets for downstream analysis.



stg\_world\_bank

stg\_global\_findex

stg\_google\_trends

stg\_chainalysis

stg\_world\_bank\_remittances



This separation makes it possible to distinguish:



What came from the source



from



What the pipeline changed or standardized



🛠️ Tools Used

Purpose	Tool

Data ingestion	Python

Data processing	Pandas

Data storage	DuckDB

Data transformation	SQL / dbt

Data quality	dbt

Version control	Git / GitHub



The technology is intentionally simple.



The focus is on using the right tools to create reliable information for analysis, rather than using technology for its own sake.



📁 Repository Structure

africa-crypto-market-data-pipeline/

│

├── data/

│   └── raw/

│       ├── chainalysis/

│       ├── global\_findex/

│       ├── google\_trends/

│       ├── world\_bank/

│       └── world\_bank\_remittances/

│

├── src/

│   └── ingestion/

│       ├── chainalysis.py

│       ├── global\_findex.py

│       ├── google\_trends.py

│       ├── world\_bank.py

│       ├── world\_bank\_remittances.py

│       └── load\_\*\_duckdb.py

│

├── dbt/

│   ├── models/

│   │   ├── sources/

│   │   └── staging/

│   ├── tests/

│   └── dbt\_project.yml

│

└── docs/

▶️ Pipeline Flow



The project can be reproduced through the following workflow:



1\. Collect public data

&#x20;       ↓

2\. Validate incoming data

&#x20;       ↓

3\. Load into DuckDB

&#x20;       ↓

4\. Register dbt sources

&#x20;       ↓

5\. Build staging models

&#x20;       ↓

6\. Run data-quality tests

&#x20;       ↓

7\. Produce analysis-ready datasets

📌 Project Outcome



The result is a reusable data foundation covering four African markets.



Instead of beginning every analysis by asking:



Where did this number come from?



the analyst can begin with:



What business question can this data help us answer?



That is the purpose of this project.



🚀 Next Stage



This repository deliberately stops at the validated data foundation.



The next stage is to use the prepared datasets for deeper market analysis and business questions.



This keeps:



Data preparation



separate from



Data interpretation and business decisions.



👩🏽‍💻 Author

Damaris Waithera



Data Analyst | Growth Analytics | FinTech \& Web3 | Emerging Markets



Building data solutions that connect business questions, markets, and reliable data.

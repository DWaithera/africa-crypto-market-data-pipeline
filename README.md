
IMG_5306(1).png
IMG_5305(1).png
IMG_5304(1).png
IMG_5303(1).png
IMG_5302(1).png
IMG_5301(1).png
IMG_5300(1).png
IMG_5299(1).png
IMG_5298(1).png
A repository simple and work done 

Perfect. Clean. ✅

This:

git diff --cached --check
returning nothing means the staged README has no whitespace errors.

README checkpoint
README created             ✅
Business-focused content  ✅
Visual headings            ✅
Pipeline explanation       ✅
Business value             ✅
Data sources               ✅
QA evidence                ✅
Repository structure       ✅
Whitespace check           ✅
Now we can safely commit it.

Next single task — commit README
Run:

git commit -m "Add project README"
Send me the commit output.

Then we'll push it to GitHub and look at the actual rendered README, because Markdown can look different on GitHub than it does in Notepad. That's where we'll make the final visual refinements.


(dbt_env) PS C:\Users\User\Desktop\africa-crypto-market-data-pipeline> git commit -m "Add project README"
[main 6cbd57b] Add project README
 1 file changed, 599 insertions(+)
 create mode 100644 README.md

Perfect. ✅ README is committed cleanly.

[main 6cbd57b] Add project README
599 insertions(+)
Next single task — publish the README
Run:

git push
Because we already set:

main → origin/main
you don't need the longer git push -u origin main command anymore.

After it finishes, open:

Africa Crypto Market Data Pipeline on GitHub

Then tell me how the rendered README looks. We want to judge the actual GitHub presentation—not the Notepad version—before we call the README finished.


its pathetic : # 🌍 Africa Crypto Market Data Pipeline

**A data pipeline for collecting, validating, and preparing public crypto-market data across four African markets for business analysis.**

[![Python](https://img.shields.io/badge/Python-Data%20Ingestion-blue)]()

[![DuckDB](https://img.shields.io/badge/DuckDB-Data%20Storage-orange)]()

[![dbt](https://img.shields.io/badge/dbt-Data%20Quality-red)]()

[![GitHub](https://img.shields.io/badge/GitHub-Version%20Control-black)]()

---

## 🎯 Project Purpose

Understanding an emerging market requires more than finding individual numbers.

Public information about African crypto markets is spread across different sources, formats, definitions, and reporting periods.

This project brings that information together for:

🇬🇭 **Ghana** · 🇰🇪 **Kenya** · 🇳🇬 **Nigeria** · 🇿🇦 **South Africa**

The goal is to create a **reliable data foundation** that can be used to understand differences between markets and support future business analysis.

### The business problem

A business evaluating an emerging market may need to understand:

- How digitally connected is the market?

- How accessible are financial services?

- How widely are digital payments used?

- What signals exist around crypto interest and adoption?

- How does the broader economic environment differ between markets?

Answering these questions requires information from multiple sources.

The challenge is making that information **consistent, traceable, and trustworthy before using it to make comparisons.**

---

## 💡 Business Value

This project turns:

**Fragmented public information**

↓

**Validated and standardized data**

↓

**Analysis-ready information**

↓

**Better business questions**

The pipeline does not make the final market decision.

Instead, it creates the data foundation needed to investigate questions such as:

**How do these markets differ?**

**What signals should a business investigate further?**

**Is the available information reliable enough to support a decision?**

---

## 🏗️ What I Built


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

You're right. That rendered README is unacceptable. The problem isn't just the content — the Markdown itself was written incorrectly, which is why GitHub is showing things like \**, \---, broken badges, and escaped characters.

I also think the previous version was too long and too documentation-heavy for the kind of portfolio you're building.

I rebuilt it around one idea:

Business problem → business value → what you built → evidence → technical proof

And cut it down from ~600 lines to 251 lines.

The new README has:
Strong visual opening

Clear business problem

Business-value section

Four-market coverage

Data-source table

Simple pipeline visual

35/35 QA result

Raw vs staging explanation

Tools

Repository structure

Project outcome

No unnecessary jargon

No fake claims

No MEPS scoring/growth strategy mixed into Repo 1

I also fixed the Markdown syntax so GitHub will render the headings, bold text, badges, tables, and diagrams properly.

I've prepared the clean README
Download the clean README

But don't upload it manually yet. Since we're working directly in your repo, the next step should be to replace the current README with this clean version, run the Markdown/Git checks, and then push it.

If you're ready, we'll do that one command at a time.


README_clean.md
Document


README_clean.md


🌍 Africa Crypto Market Data Pipeline
A data pipeline for collecting, validating, and preparing public crypto-market data across Ghana, Kenya, Nigeria, and South Africa for business analysis.






🎯 Why this project exists
African crypto-market information is available — but it is spread across different public sources, formats, indicators, and reporting periods.

For someone trying to understand a market, the first problem is therefore not "What does the data say?"

It is:

Can I bring the relevant information together, understand what each measure means, and trust the data enough to analyze it?

This project focuses on that first step.

It brings together public data for Ghana, Kenya, Nigeria, and South Africa and turns it into a consistent, validated foundation for downstream business and market analysis.

💼 Business value
The pipeline connects fragmented information to the questions a business may eventually want to investigate:

Business area	Example question
Market environment	How different are these markets in size, economic activity, and connectivity?
Financial access	How accessible are formal financial services across markets?
Digital readiness	How do internet access, smartphone adoption, and digital payments differ?
Crypto activity	Where do we see stronger signals of crypto interest or reported adoption?
Market context	How do remittance flows and broader economic indicators differ?
The pipeline does not decide which market a business should enter.

It creates a data foundation that makes those questions easier to investigate responsibly.

The value is not the number of datasets collected. The value is turning scattered information into data that can be understood, checked, and used.

🏗️ What I built
PUBLIC DATA SOURCES
        │
        ▼
   Python Ingestion
        │
        ▼
     Raw Data
        │
        ▼
      DuckDB
        │
        ▼
    dbt Staging
        │
   ┌────┴────┐
   ▼         ▼
Validation  Standardization
   │         │
   └────┬────┘
        ▼
ANALYSIS-READY DATA
        │
        ▼
 BUSINESS ANALYSIS
The workflow
1. Collect — bring together public datasets from multiple sources.

2. Preserve — keep the original data in a raw layer for traceability.

3. Validate — check expected fields, values, types, and analytical grain.

4. Standardize — create consistent staging datasets that are easier to query and compare.

5. Prepare — produce a reliable foundation for downstream analysis.

🌍 Data sources
Source	What it contributes
World Bank	Population, GDP per capita, internet access
Global Findex	Account ownership, digital payments, smartphone adoption
Google Trends	Crypto-related search interest
Chainalysis	Crypto adoption ranking
World Bank Remittances	Remittance flows relative to GDP
Markets covered
🇬🇭 Ghana · 🇰🇪 Kenya · 🇳🇬 Nigeria · 🇿🇦 South Africa

🔍 Data quality
Data quality is part of the pipeline, not something checked after the analysis.

Python + DuckDB
The ingestion layer validates incoming data and checks the expected analytical grain before loading it into the database.

dbt
The staging layer validates required fields and expected values across the five staging models.

Current result
35 / 35 dbt tests passed

PASS = 35
WARN = 0
ERROR = 0
Source-level missing values are preserved where they exist rather than silently replaced.

This matters because a missing value is something to understand before it becomes a business conclusion.

🧱 Data model
The project deliberately uses two simple layers.

Raw layer
Preserves source data and source context.

raw.raw_world_bank_indicators
raw.raw_global_findex
raw.raw_google_trends
raw.raw_chainalysis_crypto_adoption
raw.raw_world_bank_remittances
Staging layer
Creates standardized datasets for downstream analysis.

stg_world_bank
stg_global_findex
stg_google_trends
stg_chainalysis
stg_world_bank_remittances
This separation makes it clear what came from the source and what the pipeline standardized.

🛠️ Tools
Purpose	Tool
Data ingestion	Python
Data processing	Pandas
Data storage	DuckDB
Transformation	SQL / dbt
Data quality	dbt
Version control	Git / GitHub
The stack is intentionally focused. The goal is to solve the data problem clearly rather than add technology for its own sake.

📁 Repository structure
africa-crypto-market-data-pipeline/
│
├── data/raw/
│   ├── chainalysis/
│   ├── global_findex/
│   ├── google_trends/
│   ├── world_bank/
│   └── world_bank_remittances/
│
├── src/ingestion/
│   ├── chainalysis.py
│   ├── global_findex.py
│   ├── google_trends.py
│   ├── world_bank.py
│   ├── world_bank_remittances.py
│   └── load_*_duckdb.py
│
├── dbt/
│   ├── models/
│   │   ├── sources/
│   │   └── staging/
│   ├── tests/
│   └── dbt_project.yml
│
└── docs/
▶️ Pipeline flow
1. Collect public data
        ↓
2. Validate incoming data
        ↓
3. Load into DuckDB
        ↓
4. Register dbt sources
        ↓
5. Build staging models
        ↓
6. Run data-quality tests
        ↓
7. Produce analysis-ready datasets
📌 Project outcome
The result is a reusable, validated data foundation for four African markets.

That foundation can support deeper analysis without having to repeatedly start with raw files, different source structures, and unverified values.

This repository intentionally stops at data preparation and validation.

The next analytical layer can use this foundation to investigate market conditions, compare countries, and answer specific business questions.

👩🏽‍💻 Author
Damaris Waithera
Data Analyst · Growth Analytics · FinTech & Web3 · Emerging Markets

Building data solutions that connect business questions, markets, and reliable data.


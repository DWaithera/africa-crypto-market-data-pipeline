# Africa Crypto Market Data Pipeline

A data pipeline for collecting, validating, and preparing public crypto-market data across four African markets for business analysis.

## Overview

This project brings together public data for:

- Ghana
- Kenya
- Nigeria
- South Africa

The data covers crypto adoption, search interest, financial access, digital payments, internet access, economic indicators, and remittances.

The goal is to turn fragmented public data into a consistent and reliable foundation for analysis.

## What I Built

The pipeline collects data from multiple public sources, validates it, stores the raw data in DuckDB, and standardizes it using Python, SQL, and dbt.

```text
Public Data
     ↓
Python
     ↓
DuckDB
     ↓
dbt
     ↓
Validated Data
     ↓
Business Analysis

## Data Sources 

| Source | Data |
|---|---|
| World Bank | Population, GDP, internet access, remittances |
| Global Findex | Financial access, digital payments, smartphone adoption |
| Google Trends | Crypto search interest |
| Chainalysis | Crypto adoption |

## Business Value

The project creates a reliable starting point for comparing African crypto markets.

It brings information from different sources into a consistent structure so that analysts can investigate:

- Market environment
- Financial access
- Digital readiness
- Crypto interest and adoption
- Economic context

The focus is on getting the **data foundation right before using it for business analysis.**

## Data Sources

| Source | Data |
|---|---|
| World Bank | Population, GDP, internet access, remittances |
| Global Findex | Financial access, digital payments, smartphone adoption |
| Google Trends | Crypto search interest |
| Chainalysis | Crypto adoption |

## Pipeline

The project follows a simple flow:

```text
Public Data
     ↓
Python
     ↓
DuckDB
     ↓
dbt
     ↓
Validated Data
     ↓
Business Analysis




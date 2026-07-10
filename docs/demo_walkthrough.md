# PitWall Lakehouse Demo Walkthrough

This walkthrough is for a 5 to 8 minute portfolio demo.

## Before the demo

Use fixture mode for a fast smoke demo:

~~~bash
make demo-fixture
~~~

Use production mode after downloading RaceData locally:

~~~bash
make download-racedata
make demo-latest
~~~

Production source data and generated artifacts are intentionally not committed.

## Demo flow

### 1. Start with the problem

PitWall Lakehouse is a local-first Formula 1 data-engineering platform.

It turns raw public race CSV data into:

- bronze Parquet files
- silver cleaned facts and dimensions
- gold analytics marts
- audit models for source anomalies
- generated dbt quality reports
- a Streamlit demo over trusted outputs

### 2. Show the architecture

Explain the layers:

~~~text
Raw CSV archive
  -> bronze Parquet
  -> dbt bronze views
  -> dbt silver facts/dimensions
  -> dbt audit models
  -> dbt gold marts
  -> quality report
  -> Streamlit demo
~~~

### 3. Show Quality Evidence

In Streamlit, open `Quality Evidence`.

Point out:

- quality report exists
- overall passed is yes
- dbt result count is visible

### 4. Show Audit Evidence

Open `Audit Evidence`.

Show:

- duplicate lap-time grain audit
- missing pit-stop duration audit
- bronze-to-silver row-count differences

Key explanation:

The pipeline does not silently clean messy production data. It preserves audit evidence explaining what was cleaned and why row counts changed.

### 5. Show Gold Marts

Open `Gold Marts`.

Show examples:

- race summary
- driver pace
- pit-stop efficiency
- constructor reliability
- strategy windows
- stint degradation

Do not overclaim sporting conclusions unless production mode is built locally.

### 6. Close with engineering proof

Mention:

- CI validates the fixture pipeline
- production RaceData is supported locally
- Dagster supports fixture and production dataset modes
- dbt tests validate model grain and relationships
- generated data artifacts are intentionally excluded from Git

## What not to say

Do not say this is a predictive ML system.

Do not claim full historical F1 insights unless production data was built locally.

Do not describe the Streamlit app as the main product. The data platform is the product.

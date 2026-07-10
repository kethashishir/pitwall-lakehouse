{{ config(materialized='table') }}

with row_counts as (
  select
    'lap_times' as dataset_name,
    (select count(*) from {{ ref('bronze__lap_times') }}) as bronze_row_count,
    (select count(*) from {{ ref('fact_lap_time') }}) as silver_row_count,
    'Rows can differ because silver deduplicates race-driver-lap grain and drops invalid lap times.' as explanation

  union all

  select
    'pit_stops' as dataset_name,
    (select count(*) from {{ ref('bronze__pit_stops') }}) as bronze_row_count,
    (select count(*) from {{ ref('fact_pit_stop') }}) as silver_row_count,
    'Rows can differ because silver drops pit stops with missing/invalid duration milliseconds.' as explanation

  union all

  select
    'results' as dataset_name,
    (select count(*) from {{ ref('bronze__results') }}) as bronze_row_count,
    (select count(*) from {{ ref('fact_race_result') }}) as silver_row_count,
    'Rows should usually match because nullable numeric fields are preserved with try_cast.' as explanation
)

select
  dataset_name,
  bronze_row_count,
  silver_row_count,
  bronze_row_count - silver_row_count as row_count_difference,
  explanation
from row_counts

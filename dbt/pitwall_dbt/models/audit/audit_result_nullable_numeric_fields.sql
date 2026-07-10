{{ config(materialized='table') }}

with source as (
  select *
  from {{ ref('bronze__results') }}
),

field_checks as (
  select 'grid' as field_name, count(*) as source_row_count, countif(nullif(grid, '\\N') is null) as missing_count from source
  union all
  select 'positionOrder', count(*), countif(nullif(positionOrder, '\\N') is null) from source
  union all
  select 'points', count(*), countif(nullif(points, '\\N') is null) from source
  union all
  select 'laps', count(*), countif(nullif(laps, '\\N') is null) from source
  union all
  select 'milliseconds', count(*), countif(nullif(milliseconds, '\\N') is null) from source
  union all
  select 'fastestLap', count(*), countif(nullif(fastestLap, '\\N') is null) from source
  union all
  select 'rank', count(*), countif(nullif(rank, '\\N') is null) from source
  union all
  select 'fastestLapSpeed', count(*), countif(nullif(fastestLapSpeed, '\\N') is null) from source
)

select
  field_name,
  source_row_count,
  missing_count,
  round(missing_count::double / nullif(source_row_count, 0), 4) as missing_rate
from field_checks

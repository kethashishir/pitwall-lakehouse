{{ config(materialized='table') }}

with typed_laps as (
  select
    cast(raceId as integer) as race_id,
    cast(driverId as integer) as driver_id,
    cast(lap as integer) as lap_number,
    try_cast(nullif(milliseconds, '\\N') as bigint) as lap_time_milliseconds,
    nullif(time, '\\N') as lap_time
  from {{ ref('bronze__lap_times') }}
)

select
  race_id,
  driver_id,
  lap_number,
  count(*) as duplicate_row_count,
  min(lap_time_milliseconds) as fastest_duplicate_milliseconds,
  max(lap_time_milliseconds) as slowest_duplicate_milliseconds,
  string_agg(lap_time, ', ' order by lap_time) as observed_lap_times
from typed_laps
group by
  race_id,
  driver_id,
  lap_number
having count(*) > 1

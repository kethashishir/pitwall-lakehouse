{{ config(materialized='table') }}

select
  cast(raceId as integer) as race_id,
  cast(driverId as integer) as driver_id,
  cast(stop as integer) as stop_number,
  cast(lap as integer) as lap_number,
  nullif(time, '\\N') as pit_time,
  nullif(duration, '\\N') as duration_text,
  milliseconds as raw_milliseconds
from {{ ref('bronze__pit_stops') }}
where try_cast(nullif(milliseconds, '\\N') as bigint) is null

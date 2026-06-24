select
  cast(raceId as integer) as race_id,
  cast(driverId as integer) as driver_id,
  cast(stop as integer) as stop_number,
  cast(lap as integer) as lap_number,
  time as pit_time,
  duration as duration_text,
  cast(milliseconds as bigint) as pit_duration_milliseconds
from {{ ref('bronze__pit_stops') }}

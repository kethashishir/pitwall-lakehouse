select
  cast(raceId as integer) as race_id,
  cast(driverId as integer) as driver_id,
  cast(lap as integer) as lap_number,
  cast(position as integer) as position,
  time as lap_time,
  cast(milliseconds as bigint) as lap_time_milliseconds
from {{ ref('bronze__lap_times') }}

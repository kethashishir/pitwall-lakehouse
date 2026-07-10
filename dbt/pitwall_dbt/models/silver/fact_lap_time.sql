with typed_laps as (
  select
    cast(raceId as integer) as race_id,
    cast(driverId as integer) as driver_id,
    cast(lap as integer) as lap_number,
    try_cast(position as integer) as position,
    nullif(time, '\\N') as lap_time,
    try_cast(nullif(milliseconds, '\\N') as bigint) as lap_time_milliseconds
  from {{ ref('bronze__lap_times') }}
  where try_cast(nullif(milliseconds, '\\N') as bigint) is not null
),

deduplicated as (
  select
    *,
    row_number() over (
      partition by race_id, driver_id, lap_number
      order by lap_time_milliseconds, position nulls last
    ) as duplicate_rank
  from typed_laps
)

select
  race_id,
  driver_id,
  lap_number,
  position,
  lap_time,
  lap_time_milliseconds
from deduplicated
where duplicate_rank = 1

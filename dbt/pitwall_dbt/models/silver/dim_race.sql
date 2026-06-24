select
  cast(r.raceId as integer) as race_id,
  cast(r.year as integer) as season,
  cast(r.round as integer) as round,
  cast(r.circuitId as integer) as circuit_id,
  r.name as race_name,
  cast(r.date as date) as race_date,
  nullif(r.time, '\\N') as race_time_utc,
  r.url
from {{ ref('bronze__races') }} as r

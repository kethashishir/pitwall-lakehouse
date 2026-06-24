select
  cast(circuitId as integer) as circuit_id,
  circuitRef as circuit_ref,
  name as circuit_name,
  location,
  country,
  cast(lat as double) as latitude,
  cast(lng as double) as longitude,
  nullif(alt, '\\N') as altitude,
  url
from {{ ref('bronze__circuits') }}

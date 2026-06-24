select
  r.race_id,
  r.season,
  r.round,
  r.race_name,
  r.race_date,
  c.circuit_name,
  c.country,
  count(distinct rr.driver_id) as classified_drivers,
  max(rr.laps_completed) as race_laps,
  sum(rr.points) as total_points_awarded
from {{ ref('dim_race') }} as r
left join {{ ref('dim_circuit') }} as c
  on r.circuit_id = c.circuit_id
left join {{ ref('fact_race_result') }} as rr
  on r.race_id = rr.race_id
group by
  r.race_id,
  r.season,
  r.round,
  r.race_name,
  r.race_date,
  c.circuit_name,
  c.country

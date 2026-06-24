select
  ps.race_id,
  r.season,
  r.race_name,
  ps.driver_id,
  d.driver_name,
  count(*) as pit_stop_count,
  avg(ps.pit_duration_milliseconds) as avg_pit_duration_milliseconds,
  min(ps.pit_duration_milliseconds) as best_pit_duration_milliseconds,
  max(ps.pit_duration_milliseconds) as slowest_pit_duration_milliseconds,
  avg(ps.pit_duration_milliseconds)
    - min(avg(ps.pit_duration_milliseconds)) over (partition by ps.race_id)
    as avg_pit_delta_to_best_milliseconds
from {{ ref('fact_pit_stop') }} as ps
left join {{ ref('dim_race') }} as r
  on ps.race_id = r.race_id
left join {{ ref('dim_driver') }} as d
  on ps.driver_id = d.driver_id
group by
  ps.race_id,
  r.season,
  r.race_name,
  ps.driver_id,
  d.driver_name

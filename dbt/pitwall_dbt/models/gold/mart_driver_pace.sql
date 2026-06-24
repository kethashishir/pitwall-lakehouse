with lap_stats as (
  select
    race_id,
    driver_id,
    count(*) as completed_laps_in_lap_table,
    avg(lap_time_milliseconds) as avg_lap_time_milliseconds,
    min(lap_time_milliseconds) as best_lap_time_milliseconds,
    max(lap_time_milliseconds) as slowest_lap_time_milliseconds
  from {{ ref('fact_lap_time') }}
  group by race_id, driver_id
)

select
  ls.race_id,
  r.season,
  r.race_name,
  ls.driver_id,
  d.driver_name,
  ls.completed_laps_in_lap_table,
  ls.avg_lap_time_milliseconds,
  ls.best_lap_time_milliseconds,
  ls.slowest_lap_time_milliseconds,
  ls.avg_lap_time_milliseconds
    - min(ls.avg_lap_time_milliseconds) over (partition by ls.race_id)
    as avg_pace_delta_to_best_milliseconds
from lap_stats as ls
left join {{ ref('dim_race') }} as r
  on ls.race_id = r.race_id
left join {{ ref('dim_driver') }} as d
  on ls.driver_id = d.driver_id

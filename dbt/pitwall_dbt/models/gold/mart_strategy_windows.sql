with pit_laps as (
  select
    ps.race_id,
    r.season,
    r.race_name,
    ps.driver_id,
    d.driver_name,
    ps.stop_number,
    ps.lap_number as pit_lap,
    ps.pit_duration_milliseconds,
    lag(ps.lap_number) over (
      partition by ps.race_id, ps.driver_id
      order by ps.stop_number
    ) as previous_pit_lap
  from {{ ref('fact_pit_stop') }} as ps
  left join {{ ref('dim_race') }} as r
    on ps.race_id = r.race_id
  left join {{ ref('dim_driver') }} as d
    on ps.driver_id = d.driver_id
),

race_laps as (
  select
    race_id,
    max(lap_number) as observed_lap_count
  from {{ ref('fact_lap_time') }}
  group by race_id
)

select
  p.race_id,
  p.season,
  p.race_name,
  p.driver_id,
  p.driver_name,
  p.stop_number,
  p.pit_lap,
  p.previous_pit_lap,
  coalesce(p.previous_pit_lap + 1, 1) as stint_start_lap,
  p.pit_lap - 1 as stint_end_lap_before_stop,
  p.pit_duration_milliseconds,
  rl.observed_lap_count,
  round(p.pit_lap::double / nullif(rl.observed_lap_count, 0), 4) as pit_lap_fraction_of_observed_race
from pit_laps as p
left join race_laps as rl
  on p.race_id = rl.race_id

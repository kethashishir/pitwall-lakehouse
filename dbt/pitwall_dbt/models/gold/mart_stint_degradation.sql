with pit_windows as (
  select
    race_id,
    driver_id,
    stop_number,
    coalesce(previous_pit_lap + 1, 1) as stint_start_lap,
    pit_lap - 1 as stint_end_lap
  from {{ ref('mart_strategy_windows') }}
),

driver_final_laps as (
  select
    race_id,
    driver_id,
    max(lap_number) as final_observed_lap
  from {{ ref('fact_lap_time') }}
  group by race_id, driver_id
),

stints as (
  select
    race_id,
    driver_id,
    1 as stint_number,
    1 as stint_start_lap,
    coalesce(min(pit_lap) - 1, max(lap_number)) as stint_end_lap
  from (
    select
      lt.race_id,
      lt.driver_id,
      lt.lap_number,
      sw.pit_lap
    from {{ ref('fact_lap_time') }} as lt
    left join {{ ref('mart_strategy_windows') }} as sw
      on lt.race_id = sw.race_id
      and lt.driver_id = sw.driver_id
  )
  group by race_id, driver_id

  union all

  select
    race_id,
    driver_id,
    stop_number + 1 as stint_number,
    pit_lap + 1 as stint_start_lap,
    lead(pit_lap, 1, final_observed_lap + 1) over (
      partition by race_id, driver_id
      order by stop_number
    ) - 1 as stint_end_lap
  from {{ ref('mart_strategy_windows') }} as sw
  left join driver_final_laps as fl
    using (race_id, driver_id)
),

stint_laps as (
  select
    s.race_id,
    r.season,
    r.race_name,
    s.driver_id,
    d.driver_name,
    s.stint_number,
    s.stint_start_lap,
    s.stint_end_lap,
    lt.lap_number,
    lt.lap_time_milliseconds,
    lt.lap_number - s.stint_start_lap + 1 as lap_in_stint
  from stints as s
  left join {{ ref('fact_lap_time') }} as lt
    on s.race_id = lt.race_id
    and s.driver_id = lt.driver_id
    and lt.lap_number between s.stint_start_lap and s.stint_end_lap
  left join {{ ref('dim_race') }} as r
    on s.race_id = r.race_id
  left join {{ ref('dim_driver') }} as d
    on s.driver_id = d.driver_id
)

select
  race_id,
  season,
  race_name,
  driver_id,
  driver_name,
  stint_number,
  stint_start_lap,
  stint_end_lap,
  count(lap_number) as observed_laps_in_stint,
  min(lap_time_milliseconds) as best_lap_time_milliseconds,
  max(lap_time_milliseconds) as slowest_lap_time_milliseconds,
  avg(lap_time_milliseconds) as avg_lap_time_milliseconds,
  case
    when count(lap_number) >= 2 then
      regr_slope(lap_time_milliseconds, lap_in_stint)
    else null
  end as lap_time_degradation_slope_ms_per_lap
from stint_laps
group by
  race_id,
  season,
  race_name,
  driver_id,
  driver_name,
  stint_number,
  stint_start_lap,
  stint_end_lap

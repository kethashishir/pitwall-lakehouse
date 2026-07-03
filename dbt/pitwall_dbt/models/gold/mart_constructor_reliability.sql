with result_status as (
  select
    rr.race_id,
    r.season,
    r.race_name,
    rr.constructor_id,
    c.constructor_name,
    rr.driver_id,
    rr.result_id,
    rr.status_id,
    s.status,
    case
      when lower(s.status) = 'finished' then 1
      else 0
    end as finished_flag,
    rr.laps_completed
  from {{ ref('fact_race_result') }} as rr
  left join {{ ref('dim_race') }} as r
    on rr.race_id = r.race_id
  left join {{ ref('dim_constructor') }} as c
    on rr.constructor_id = c.constructor_id
  left join {{ ref('dim_status') }} as s
    on rr.status_id = s.status_id
)

select
  season,
  constructor_id,
  constructor_name,
  count(*) as classified_entries,
  sum(finished_flag) as finished_entries,
  count(*) - sum(finished_flag) as non_finished_entries,
  round(sum(finished_flag)::double / nullif(count(*), 0), 4) as finish_rate,
  avg(laps_completed) as avg_laps_completed
from result_status
group by
  season,
  constructor_id,
  constructor_name

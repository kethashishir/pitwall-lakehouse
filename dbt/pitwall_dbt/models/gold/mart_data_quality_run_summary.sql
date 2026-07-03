with bronze_counts as (
  select 'bronze__drivers' as model_name, count(*) as row_count from {{ ref('bronze__drivers') }}
  union all
  select 'bronze__constructors', count(*) from {{ ref('bronze__constructors') }}
  union all
  select 'bronze__circuits', count(*) from {{ ref('bronze__circuits') }}
  union all
  select 'bronze__races', count(*) from {{ ref('bronze__races') }}
  union all
  select 'bronze__results', count(*) from {{ ref('bronze__results') }}
  union all
  select 'bronze__lap_times', count(*) from {{ ref('bronze__lap_times') }}
  union all
  select 'bronze__pit_stops', count(*) from {{ ref('bronze__pit_stops') }}
  union all
  select 'bronze__qualifying', count(*) from {{ ref('bronze__qualifying') }}
  union all
  select 'bronze__seasons', count(*) from {{ ref('bronze__seasons') }}
  union all
  select 'bronze__status', count(*) from {{ ref('bronze__status') }}
),

silver_counts as (
  select 'dim_driver' as model_name, count(*) as row_count from {{ ref('dim_driver') }}
  union all
  select 'dim_constructor', count(*) from {{ ref('dim_constructor') }}
  union all
  select 'dim_circuit', count(*) from {{ ref('dim_circuit') }}
  union all
  select 'dim_race', count(*) from {{ ref('dim_race') }}
  union all
  select 'dim_status', count(*) from {{ ref('dim_status') }}
  union all
  select 'fact_race_result', count(*) from {{ ref('fact_race_result') }}
  union all
  select 'fact_lap_time', count(*) from {{ ref('fact_lap_time') }}
  union all
  select 'fact_pit_stop', count(*) from {{ ref('fact_pit_stop') }}
),

gold_counts as (
  select 'mart_race_summary' as model_name, count(*) as row_count from {{ ref('mart_race_summary') }}
  union all
  select 'mart_driver_pace', count(*) from {{ ref('mart_driver_pace') }}
  union all
  select 'mart_pit_stop_efficiency', count(*) from {{ ref('mart_pit_stop_efficiency') }}
  union all
  select 'mart_constructor_reliability', count(*) from {{ ref('mart_constructor_reliability') }}
  union all
  select 'mart_strategy_windows', count(*) from {{ ref('mart_strategy_windows') }}
  union all
  select 'mart_stint_degradation', count(*) from {{ ref('mart_stint_degradation') }}
)

select
  'bronze' as layer,
  model_name,
  row_count
from bronze_counts

union all

select
  'silver' as layer,
  model_name,
  row_count
from silver_counts

union all

select
  'gold' as layer,
  model_name,
  row_count
from gold_counts

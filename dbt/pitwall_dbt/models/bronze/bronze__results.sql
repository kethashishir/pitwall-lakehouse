select *
from read_parquet('data/bronze/{{ var("bronze_dataset") }}/results.parquet')

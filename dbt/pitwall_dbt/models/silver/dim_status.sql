select
  cast(statusId as integer) as status_id,
  status
from {{ ref('bronze__status') }}

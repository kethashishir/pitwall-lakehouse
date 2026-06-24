select
  cast(constructorId as integer) as constructor_id,
  constructorRef as constructor_ref,
  name as constructor_name,
  nationality,
  url
from {{ ref('bronze__constructors') }}

select
  cast(driverId as integer) as driver_id,
  driverRef as driver_ref,
  nullif(number, '\\N') as permanent_number,
  nullif(code, '\\N') as driver_code,
  forename,
  surname,
  forename || ' ' || surname as driver_name,
  cast(dob as date) as date_of_birth,
  nationality,
  url
from {{ ref('bronze__drivers') }}

select
    city,
    date::date as weather_date,
    temperature::float as temperature,
    precipitation::float as precipitation
from {{ source('raw', 'raw_weather') }}

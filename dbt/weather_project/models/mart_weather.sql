select
    weather_date,
    city,
    avg(temperature) as avg_temp,
    max(temperature) as max_temp,
    min(temperature) as min_temp,
    sum(precipitation) as total_rain,
    case 
        when sum(precipitation) > 50 then 'Heavy Rain'
        when sum(precipitation) between 10 and 50 then 'Moderate Rain'
        else 'Light/No Rain'
    end as rain_category
from {{ ref('stg_weather') }}
group by weather_date, city
order by weather_date, city

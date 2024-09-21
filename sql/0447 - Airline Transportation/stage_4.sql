select
    if(plane_type like 'Boeing%', 'Boeing', 'Airbus') as aircraft_type,
    sum(timestampdiff(minute, time_out, time_in)) / count(*) as avg_flight_duration,
    count(*) as num_flights
from
    Trip
group by
    aircraft_type;

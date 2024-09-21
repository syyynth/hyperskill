select
    concat(town_from, '-', town_to) as route,
    sum(timestampdiff(minute, time_out, time_in)) / count(*) as avg_flight_duration,
    count(ID_psg) as total_passengers,
    sum(timestampdiff(minute, time_out, time_in)) * .6 as total_income
from Trip
    join Pass_in_trip using (trip_no)
group by
    route
order by
    total_income desc;

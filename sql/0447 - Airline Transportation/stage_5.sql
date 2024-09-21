with ranked as (
    select
        ac.company_name,
        t.town_from,
        t.town_to,
        sum(timestampdiff(minute, t.time_out, t.time_in)) / count(*) as avg_flight_duration,
        row_number() over (partition by ac.company_name order by sum(timestampdiff(minute, t.time_out, t.time_in)) / count(*) desc) as pos
    from
        Airline_company ac
    join
        Trip t using (ID_comp)
    group by
        ac.company_name,
        t.town_from,
        t.town_to
)
select
    company_name,
    town_from as departure_city,
    town_to as arrival_city,
    avg_flight_duration
from
    ranked
where
    pos < 3;

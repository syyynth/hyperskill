select
    passenger_name,
    count(*) as num_flights,
    company_name
from Passenger
    join Pass_in_trip using (ID_psg)
    join Trip using (trip_no)
    join Airline_company using (ID_comp)
group by
    ID_psg,
    company_name
having
    num_flights > 1;

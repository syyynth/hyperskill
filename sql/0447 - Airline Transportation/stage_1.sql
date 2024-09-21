alter table Pass_in_trip
    modify trip_date date;

update Pass_in_trip
    set trip_date = date(trip_date);

select * from Pass_in_trip;

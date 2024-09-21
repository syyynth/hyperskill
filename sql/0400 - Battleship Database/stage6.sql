select
    s.class,
    sum(o.result = 'damaged') as num_damaged,
    sum(o.result = 'sunk') as num_sunk,
    sum(o.result = 'OK') as num_ok
from
    Ships s
join
    Classes c on s.class = c.class
join
    Outcomes o on s.name = o.ship
group by
    s.class
having
    count(*) >= 3;

select
    s.id,
    s.name
from
    Square s
left join
    Painting p
on
    s.id = p.square_id
where
    p.square_id is null
order by
    s.name desc;

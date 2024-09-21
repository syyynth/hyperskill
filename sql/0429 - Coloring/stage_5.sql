select
    distinct s.name
from
    Spray s
join
    Painting p
on
    s.id = p.spray_id
where
    color = 'R'
group by
    p.square_id, s.name
having
    count(color = 'R') > 1 and count(color = 'B')
order by
    s.name;
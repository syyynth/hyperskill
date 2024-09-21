select
    s.color,
    sum(p.volume) as total_paint_used
from
    Painting p
join
    Spray s
on
    s.id = p.spray_id
group by
    s.color
order by
    total_paint_used;

select
   s.id,
   255 - coalesce(sum(p.volume), 0) as remaining_volume
from
    Spray s
left join
    Painting p
on
    s.id = p.spray_id
group by
    s.id
order by
    s.id;

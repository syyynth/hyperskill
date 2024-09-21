select
    p.square_id,
    count(distinct p.spray_id) as num_sprays
from 
    Painting p
join 
    Spray s on s.id = p.spray_id
group by
    p.square_id
having
    sum(if(s.color = 'R', p.volume, 0)) = 255
    and sum(if(s.color = 'G', p.volume, 0)) = 255
    and sum(if(s.color = 'B', p.volume, 0)) = 255
order by
    p.square_id;

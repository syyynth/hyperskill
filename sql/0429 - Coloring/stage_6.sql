with empty_cans as (
    select spray_id
    from Painting
    group by spray_id
    having sum(volume) = 255
)
select sq.name
from Painting p
join Spray s on s.id = p.spray_id
join Square sq on p.square_id = sq.id
join empty_cans ec on ec.spray_id = p.spray_id
group by p.square_id
having sum(if(s.color = 'R', p.volume, 0)) = 255
   and sum(if(s.color = 'G', p.volume, 0)) = 255
   and sum(if(s.color = 'B', p.volume, 0)) = 255
order by p.square_id;

select 
    `country`,
    count(*) as `num_battleships`
from 
    `Classes`
where 
    `type` = 'bb'
group by 
    `country`
order by 
    `num_battleships` desc
limit 1;

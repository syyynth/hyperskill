select
    `Classes`.`country` as `country`, 
    count(*) as `num_sunk_ships`
from
    `Outcomes`
join
    `Ships` on `Outcomes`.`ship` = `Ships`.`name`
join
    `Classes` on `Classes`.`class` = `Ships`.`class`
where
    `Outcomes`.`result` = 'sunk'
group by
    `Classes`.`country`
order by
    `num_sunk_ships` desc;

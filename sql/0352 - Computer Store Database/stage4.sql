with pc_laptop as (
    select model, speed, price from PC
    union all
    select model, speed, price from Laptop
),
min_speed as (
    select min(speed) as speed from pc_laptop
)
select
    p.maker,
    pl.model,
    pl.speed,
    pl.price
from
    Product p
join
    pc_laptop pl using (model)
join
    min_speed ms using (speed);
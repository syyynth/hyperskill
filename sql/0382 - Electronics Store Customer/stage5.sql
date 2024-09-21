with max_pc_price as (
    select price from PC order by price desc limit 1
),
avg_laptop as (
    select avg(price) as price from Laptop
)
select
    l.model,
    p.maker,
    l.price,
    l.price - max_pc_price.price as price_difference_max_pc,
    l.price - avg_laptop.price as price_difference_avg_laptop
from
    Laptop l
join
    Product p using(model),
    max_pc_price,
    avg_laptop
where
    l.price > max_pc_price.price;
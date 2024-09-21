select
    p.maker,
    p.model,
    l.hd,
    l.speed,
    l.price
from 
    Laptop l
join
    Product p
on
    l.model=p.model
where
    l.hd >= 1000
order by
    l.hd,
    l.speed desc,
    l.price;
select
    maker,
    sum(price) as total_price
from
    Laptop
join
    Product using (model)
group by
    maker
order by
    total_price;

select
    maker,
    sum(type = 'pc') as pc_count,
    sum(type = 'laptop') as laptop_count
from
    Product
group by
    maker
having
    pc_count * laptop_count;
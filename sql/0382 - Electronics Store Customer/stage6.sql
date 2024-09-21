with ranked as (
    select 
        pc_code,
        model,
        speed,
        ram,
        hd,
        cd,
        price,
        dense_rank() over (partition by ram order by price desc) as place
    from 
        PC
)
select
    pc_code,
    model,
    speed,
    ram,
    hd,
    cd,
    price
from
    ranked
where
    place = 2;

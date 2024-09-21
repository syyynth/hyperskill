select
    pc_code,
    model,
    speed,
    ram
from
    PC
where
    ram >= 16
order by
    ram,
    speed desc;

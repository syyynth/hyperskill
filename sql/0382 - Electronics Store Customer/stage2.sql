select
    round(avg(price), 2)
from
    Printer
where
    color = 'C' and type = 'Inkjet';
select
    count(*) as number_of_unique_makers
from (
    select
        count(model)
    from
        Product
    group by
        maker
    having
        count(maker) = 1
) number_of;
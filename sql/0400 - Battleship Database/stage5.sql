select
    r.name, 
    r.launched, 
    r.country
from (
    select
        s.name, 
        s.launched, 
        c.country,
        min(s.launched) over (partition by c.country) as min_launched
    from Ships s
    join Classes c on s.class = c.class
    where s.name <> 'HMS Queen Elizabeth'
) as r
where r.launched = r.min_launched
group by r.name
order by r.launched;

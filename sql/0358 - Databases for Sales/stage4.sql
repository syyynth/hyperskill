select
    concat(e.first_name, ' ', e.last_name) as employee_name,
    e.position,
    date_format(s.sale_date, '%M %Y') as month_year,
    case
        when (sum(s.total_price) / (select sum(total_price) from sales)) * 100 < 5 then 0
        when (sum(s.total_price) / (select sum(total_price) from sales)) * 100 between 5 and 10 then 2000
        when (sum(s.total_price) / (select sum(total_price) from sales)) * 100 between 10 and 20 then 5000
        when (sum(s.total_price) / (select sum(total_price) from sales)) * 100 between 20 and 30 then 10000
        when (sum(s.total_price) / (select sum(total_price) from sales)) * 100 between 30 and 40 then 15000
        else 25000
    end as employee_bonus
from
    employees e
join
    sales s using (employee_id)
where
    e.position = 'Sales Associate'
group by
    e.employee_id, month_year;

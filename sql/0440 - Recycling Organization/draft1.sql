with combined as (
    select 'Company 1 Income' as company_name, money_in from Income_one_day
    union all
    select 'Company 2 Income' as company_name, money_in from Income
),
stats as (
    select company_name, money_in,
           row_number() over (partition by company_name order by money_in) as row_num,
           count(*) over (partition by company_name) as total_rows
    from combined
),
median as (
    select company_name, round(avg(money_in), 2) as median
    from stats
    where row_num in (floor((total_rows + 1) / 2), ceil((total_rows + 1) / 2))
    group by company_name
),
ranked as (
    select company_name, money_in, ntile(2) over (partition by company_name order by money_in desc) as gr
    from combined
),
quartiles as (
    select company_name, round(avg(money_in), 2) as q_value, gr
    from (
        select company_name, money_in, gr,
               row_number() over (partition by company_name, gr order by money_in) as row_num,
               count(*) over (partition by company_name, gr) as total_rows
        from ranked
    ) t
    where row_num in (floor((total_rows + 1) / 2), ceil((total_rows + 1) / 2))
    group by company_name, gr
),
q1 as (
    select company_name, q_value as q1
    from quartiles
    where gr = 1
),
q3 as (
    select company_name, q_value as q3
    from quartiles
    where gr = 2
),
mean as (
    select company_name, round(avg(money_in), 2) as mean
    from combined
    group by company_name
),
total_range as (
    select company_name, round(max(money_in) - min(money_in), 2) as total_range
    from combined
    group by company_name
),
iqr as (
    select q1.company_name, round(q1.q1 - q3.q3, 2) as interquartile_range
    from q1
    join q3 using (company_name)
),
stdev as (
    select company_name, round(stddev(money_in), 2) as standard_deviation
    from combined
    group by company_name
),
var as (
    select company_name, round(variance(money_in), 2) as variance
    from combined
    group by company_name
)
select
    mean.company_name,
    mean.mean,
    median.median,
    total_range.total_range,
    iqr.interquartile_range,
    stdev.standard_deviation,
    var.variance
from mean
join median using (company_name)
join total_range using (company_name)
join iqr using (company_name)
join stdev using (company_name)
join var using (company_name);
with stats_A as (
    select
        money_in,
        row_number() over (order by money_in) as row_num,
        count(*) over () as total_rows
    from Income_one_day
),
median_A as (
    select round(avg(money_in), 2) as median
    from stats_A
    where row_num in (floor((total_rows + 1) / 2), ceil((total_rows + 1) / 2))
),
ranked_A as (
    select
        money_in, 
        ntile(2) over (order by money_in desc) as gr
    from Income_one_day
),
q1_A as (select avg(money_in) as median
              from (select
                    money_in,
                    row_number() over (order by money_in) as row_num,
                    count(*) over () as total_rows
               from ranked_A where gr = 1) t
where row_num in (floor((total_rows + 1) / 2), ceil((total_rows + 1) / 2))),
q2_A as (select avg(money_in) as median
              from (select
                    money_in,
                    row_number() over (order by money_in) as row_num,
                    count(*) over () as total_rows
               from ranked_A where gr = 2) t
where row_num in (floor((total_rows + 1) / 2), ceil((total_rows + 1) / 2))),
mean_A as (
    select round(avg(money_in), 2) as mean from Income_one_day
),
total_range_A as (
    select round(max(money_in) - min(money_in), 2) as total_range from Income_one_day
),
iqr_A as (
    select round(q1_A.median - q2_A.median, 2) as interquartile_range from q1_A, q2_A
),
stdev_A as (
    select round(std(money_in), 2) as standard_deviation from Income_one_day
),
var_A as (
    select round(variance(money_in), 2) as variance from Income_one_day
),
stats_B as (
    select
        money_in,
        row_number() over (order by money_in) as row_num,
        count(*) over () as total_rows
    from Income
),
median_B as (
    select round(avg(money_in), 2) as median
    from stats_B
    where row_num in (floor((total_rows + 1) / 2), ceil((total_rows + 1) / 2))
),
ranked_B as (
    select
        money_in, 
        ntile(2) over (order by money_in desc) as gr
    from Income
),
q1_B as (select avg(money_in) as median
              from (select
                    money_in,
                    row_number() over (order by money_in) as row_num,
                    count(*) over () as total_rows
               from ranked_B where gr = 1) t
where row_num in (floor((total_rows + 1) / 2), ceil((total_rows + 1) / 2))),
q2_B as (select avg(money_in) as median
              from (select
                    money_in,
                    row_number() over (order by money_in) as row_num,
                    count(*) over () as total_rows
               from ranked_B where gr = 2) t
where row_num in (floor((total_rows + 1) / 2), ceil((total_rows + 1) / 2))),
mean_B as (
    select round(avg(money_in), 2) as mean from Income
),
total_range_B as (
    select round(max(money_in) - min(money_in), 2) as total_range from Income
),
iqr_B as (
    select round(q1_B.median - q2_B.median, 2) as interquartile_range from q1_B, q2_B
),
stdev_B as (
    select round(std(money_in), 2) as standard_deviation from Income
),
var_B as (
    select round(variance(money_in), 2) as variance from Income
)
select 'Company 1 Income' as company_name,
        mean_A.mean as mean,
        median_A.median as median,
        total_range_A.total_range as total_range,
        iqr_A.interquartile_range as interquartile_range,
        stdev_A.standard_deviation as standard_deviation,
        var_A.variance as variance
from mean_A, median_A, total_range_A, iqr_A, stdev_A, var_A
union all
select 'Company 2 Income' as company_name,
        mean_B.mean as mean,
        median_B.median as median,
        total_range_B.total_range as total_range,
        iqr_B.interquartile_range as interquartile_range,
        stdev_B.standard_deviation as standard_deviation,
        var_B.variance as variance
from mean_B, median_B, total_range_B, iqr_B, stdev_B, var_B;
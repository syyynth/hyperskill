with income as (
    select
        p.ID_psg,
        p.passenger_name,
        sum(timestampdiff(minute, t.time_out, t.time_in)) * .6 as passenger_income_dollars
    from
        Passenger p
        join Pass_in_trip pit using (ID_psg)
        join Trip t using (trip_no)
    group by
        p.ID_psg, p.passenger_name
),
income_with_totals as (
    select
        *,
        round(
            100 * sum(passenger_income_dollars) over (order by passenger_income_dollars desc)
                / sum(passenger_income_dollars) over (), 2
        ) as cumulative_share_percent
    from
        income
)
select
    *,
    case
        when cumulative_share_percent <= 80 then 'A'
        when cumulative_share_percent <= 95 then 'B'
        else 'C'
    end as category
from
    income_with_totals;

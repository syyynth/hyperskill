drop function if exists TaxOwed;
drop procedure if exists EmployeeTotalPay;
drop procedure if exists PayrollReport;

DELIMITER //

create function TaxOwed (
    income float
)
returns float
reads sql data
begin
    set @tax := (select
        case
            when income <= 11000 then income * .1
            when income <= 44725 then 1100 + (income - 11000) * .12
            when income <= 95375 then 5147 + (income - 44725) * .22
            when income <= 182100 then 16290 + (income - 95375) * .24
            when income <= 231250 then 37104 + (income - 182100) * .32
            when income <= 578125 then 52382 + (income - 231250) * .35
            else 174238.23 + income * .37
        end as tax);
    return @tax;
end // 


create procedure EmployeeTotalPay(
    in first_name varchar(45),
    in last_name varchar(45),
    in total_hours int,
    in normal_hours int,
    in overtime_rate float,
    in max_overtime_pay float,
    out total_pay float
)
begin
    declare base_pay double;
    declare hourly_rate double;
    declare overtime_hours int default greatest(0, total_hours - normal_hours);
    declare overtime_pay double;
    declare job_type varchar(45);

    select j.hourly_rate into hourly_rate
    from employees e
    join jobs j on e.job_id = j.id
    where e.first_name = first_name and e.last_name = last_name;

    select j.type into job_type
    from employees e
    join jobs j on e.job_id = j.id
    where e.first_name = first_name and e.last_name = last_name;

    set base_pay = hourly_rate * least(total_hours, normal_hours);
    set overtime_pay = if(job_type = 'Full Time', least(overtime_hours * hourly_rate * overtime_rate, max_overtime_pay), 0);
    set total_pay = base_pay + overtime_pay;
end //

create procedure PayrollReport (
    in dep_name varchar(45)
)
begin
    select
        concat(first_name, ' ', last_name) as full_names
    from
        employees;
end //

DELIMITER ;

call EmployeeTotalPay('Philip', 'Wilson', 2160, 2080, 1.5, 6000, @total_pay_philip);
call EmployeeTotalPay('Daisy', 'Diamond', 2100, 2080, 1.5, 6000, @total_pay_daisy);

select
    TaxOwed(@total_pay_philip) as `Philip Wilson`,
    TaxOwed(@total_pay_daisy) as `Daisy Diamond`;

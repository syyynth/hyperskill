drop procedure if exists EmployeeTotalPay;

DELIMITER //

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

DELIMITER ;

call EmployeeTotalPay('Philip', 'Wilson', 2160, 2080, 1.5, 6000, @total_pay_philip);
call EmployeeTotalPay('Daisy', 'Diamond', 2100, 2080, 1.5, 6000, @total_pay_daisy);

select
    @total_pay_philip as `Philip Wilson`,
    @total_pay_daisy as `Daisy Diamond`;

drop function if exists TaxOwed;
drop procedure if exists EmployeeTotalPay;
drop procedure if exists PayrollReport;

drop table if exists working_hours;

create table working_hours (
    first_name varchar(45),
    last_name  varchar(45),
    hours      int,
    department varchar(45)
);

insert into working_hours (first_name, last_name, hours, department)
values
    ('Dixie', 'Herda', 2095, 'City Ethics Commission'),
    ('Stephen', 'West', 2091, 'City Ethics Commission'),
    ('Philip', 'Wilson', 2160, 'City Ethics Commission'),
    ('Robin', 'Walker', 2083, 'City Ethics Commission'),
    ('Antoinette', 'Matava', 2115, 'City Ethics Commission'),
    ('Courtney', 'Walker', 2206, 'City Ethics Commission'),
    ('Gladys', 'Bosch', 2080, 'City Ethics Commission');

DELIMITER //

create function TaxOwed(income float)
    returns float
    deterministic
begin
    return
        case
            when income <= 11000 then income * .1
            when income <= 44725 then 1100 + (income - 11000) * .12
            when income <= 95375 then 5147 + (income - 44725) * .22
            when income <= 182100 then 16290 + (income - 95375) * .24
            when income <= 231250 then 37104 + (income - 182100) * .32
            when income <= 578125 then 52382 + (income - 231250) * .35
            else 174238.23 + income * .37
        end;
end //

create procedure EmployeeTotalPay(
    in first_name varchar(45),
    in last_name varchar(45),
    in total_hours int,
    in normal_hours int,
    in overtime_rate float,
    in max_overtime_pay float,
    out base_pay double,
    out overtime_pay double,
    out total_pay double
)
begin
    declare hourly_rate double;
    declare overtime_hours int default greatest(0, total_hours - normal_hours);
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
    set overtime_pay = if(job_type = 'Full Time',
                          least(overtime_hours * hourly_rate * overtime_rate, max_overtime_pay),
                          0);
    set total_pay = base_pay + overtime_pay;
end //

create procedure PayrollReport(in dept_name varchar(45))
begin
    declare done int default false;
    declare emp_first_name, emp_last_name varchar(255);
    declare emp_hours int;
    declare emp_base_hours int default 2080;
    declare emp_overtime_rate double default 1.5;
    declare emp_base_salary double default 6000;
    declare tax_owed, net_income double;
    declare full_name varchar(255);

    declare cur cursor for
        select first_name, last_name, hours from working_hours where department = dept_name;

    declare continue handler for not found set done = true;

    drop temporary table if exists payroll_details;
    create temporary table payroll_details (
        full_names   varchar(255),
        base_pay     double,
        overtime_pay double,
        total_pay    double,
        tax_owed     double,
        net_income   double
    );

    open cur;

    read_loop: loop
        fetch cur into emp_first_name, emp_last_name, emp_hours;

        if done then
            leave read_loop;
        end if;

        call EmployeeTotalPay(
            emp_first_name,
            emp_last_name,
            emp_hours,
            emp_base_hours,
            emp_overtime_rate,
            emp_base_salary,
            @base_pay,
            @overtime_pay,
            @total_pay
        );

        set tax_owed = taxowed(@total_pay);
        set net_income = @total_pay - tax_owed;
        set full_name = concat(emp_first_name, ' ', emp_last_name);

        insert into payroll_details
        values
            (full_name, @base_pay, @overtime_pay, @total_pay, tax_owed, net_income);

    end loop;

    close cur;

    select * from payroll_details order by base_pay desc, full_names;

    drop temporary table payroll_details;
end //

DELIMITER ;

call PayrollReport('City Ethics Commission');

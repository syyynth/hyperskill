drop procedure if exists GetEmployeesByDept;

DELIMITER //
create procedure GetEmployeesByDept(
    in dep_name varchar(45)
)
begin
    select
        e.first_name,
        e.last_name,
        j.title as job_title
    from
        employees e
    join
        departments d on d.id = e.department_id
    join
        jobs j on j.id = e.job_id
    where
        d.name = dep_name
    order by
        e.first_name;
end //
DELIMITER ;

call GetEmployeesByDept('Office of Finance');

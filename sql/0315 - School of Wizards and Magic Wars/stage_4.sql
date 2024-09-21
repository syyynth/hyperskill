select
    s.name,
    d.department_name
from students s
join student_subject subj
    using (student_id)
join department d
    using (department_id)
group by
    s.student_id
having
    avg(subj.result) > 4.5
order by
    s.name;

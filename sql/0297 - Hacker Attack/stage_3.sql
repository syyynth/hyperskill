.import person.csv person --csv
.import teacher.csv teacher --csv
.mode column

create table student as
select
    person_id,
    null as grade_code
from person left join teacher
     using (person_id)
where class_code is null;

select * from student order by person_id limit 5;

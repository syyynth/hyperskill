.import person.csv person --csv
.import teacher.csv teacher --csv
.mode column

select
    person_id,
    full_name
from person left join teacher
     using (person_id)
where class_code is null
order by full_name
limit 5;

select
    COUNT(person_id)
from person left join teacher
     using (person_id)
where class_code is null;

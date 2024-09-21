.import person.csv person --csv
.mode column

select person_id, full_name from person order by 1 limit 5;

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

create table score1 (person_id text, score integer);
create table score2 (person_id text, score integer);
create table score3 (person_id text, score integer);

.import score1.csv score1 --csv --skip 1
.import score2.csv score2 --csv --skip 1
.import score3.csv score3 --csv --skip 1

create table score (person_id text, score integer);

insert into score
select person_id, score from score1
union all
select person_id, score from score2
union all
select person_id, score from score3
join
student using (person_id);

drop table score1;
drop table score2;
drop table score3;

select * from score order by person_id limit 5;

select
    person_id,
    count(score) as `count(score)`
from
    score
group by
    person_id
having
    `count(score)` = 3
order by
    person_id
limit 5;

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

update student
set grade_code = (
    select
        case score_count
            when 3 then 'GD-12'
            when 2 then 'GD-11'
            when 1 then 'GD-10'
            else 'GD-09'
        end
    from (
        select count(score) as score_count
        from score
        where score.person_id = student.person_id
    )
);

select
    person_id,
    round(avg(score), 2) as avg_score
from
    student join score using (person_id)
where
    grade_code = 'GD-12'
group by
    person_id
order by
    avg_score desc;

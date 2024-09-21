select
    st.name,
    sum(a.bonus) as `bonus point`
from students st
join student_achievement sa
     using (student_id)
join achievement a
     using (achievement_id)
group by
    st.student_id
order by
    `bonus point` desc
limit 4;

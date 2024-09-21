select
    st.name,
    iif(avg(subj.result) > 3.5, 'above average', 'below average') as best
from students st
join student_subject subj
     using (student_id)
group by
    st.student_id
order by
    st.name;

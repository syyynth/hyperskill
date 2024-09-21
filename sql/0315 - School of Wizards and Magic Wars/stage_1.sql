select
    st.name
from students st
join student_subject subj
     using (student_id)
where
    st.grade = 3
group by
    st.student_id
having
    min(subj.result) = 5
order by 1;

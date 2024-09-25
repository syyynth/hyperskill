import pandas as pd

files = {
    'A': '../Data/A_office_data.xml',
    'B': '../Data/B_office_data.xml',
    'HR': '../Data/hr_data.xml'
}

office_data = {key: pd.read_xml(file) for key, file in files.items()}
office_data['A'].index = 'A' + office_data['A']['employee_office_id'].astype(str)
office_data['B'].index = 'B' + office_data['B']['employee_office_id'].astype(str)
office_data['HR'].index = office_data['HR']['employee_id']

office_AB = pd.concat([office_data['A'], office_data['B']])

merged = (
    office_AB
    .join(office_data['HR'], how='inner')
    .drop(['employee_office_id', 'employee_id'], axis=1)
    .sort_index()
)


def stage_3():
    ans1 = merged.nlargest(10, 'average_monthly_hours')['Department'].tolist()
    ans2 = merged.query('Department == "IT" & salary == "low"')['number_project'].sum()
    ans3 = merged.loc[['A4', 'B7064', 'A3033'], ['last_evaluation', 'satisfaction_level']].values.tolist()

    print(ans1)
    print(ans2)
    print(ans3)


def stage_4():
    def count_bigger_5(series):
        return (series > 5).sum()

    stats = merged.groupby('left').agg({
        'Work_accident': 'mean',
        'last_evaluation': ['mean', 'std'],
        'number_project': ['median', count_bigger_5],
        'time_spend_company': ['mean', 'median']
    }).round(2)

    ans = stats.to_dict()

    print(ans)


def stage_5():
    pivot_table_1 = merged.pivot_table(
        index='Department',
        columns=['left', 'salary'],
        values='average_monthly_hours',
        aggfunc='median'
    )

    cond1 = pivot_table_1[(0, 'high')] < pivot_table_1[(0, 'medium')]
    cond2 = pivot_table_1[(1, 'low')] < pivot_table_1[(1, 'high')]
    ans1 = pivot_table_1[cond1 | cond2].to_dict()

    pivot_table_2 = merged.pivot_table(
        index='time_spend_company',
        columns='promotion_last_5years',
        values=['last_evaluation', 'satisfaction_level'],
        aggfunc=['min', 'max', 'mean']
    )
    cond = pivot_table_2[('mean', 'last_evaluation', 0)] > pivot_table_2[('mean', 'last_evaluation', 1)]
    ans2 = pivot_table_2[cond].to_dict()

    print(ans1)
    print(ans2)


stage_5()

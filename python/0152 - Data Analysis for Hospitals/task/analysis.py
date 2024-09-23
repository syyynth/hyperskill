import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def load_and_clean_data():
    general = pd.read_csv('test/general.csv', index_col=0)
    prenatal = pd.read_csv('test/prenatal.csv', index_col=0, header=0, names=general.columns)
    sports = pd.read_csv('test/sports.csv', index_col=0, header=0, names=general.columns)

    df = pd.concat([general, prenatal, sports], ignore_index=True)
    gender_labels = {'man': 'm', 'woman': 'f', 'female': 'f', 'male': 'm'}
    na_wildcards = ['bmi', 'diagnosis', 'blood_test', 'ecg', 'ultrasound', 'mri', 'xray', 'children', 'months']

    df.dropna(how='all', inplace=True)
    df.replace({'gender': gender_labels}, inplace=True)
    df.loc[df.hospital == 'prenatal', 'gender'] = df.loc[df.hospital == 'prenatal', 'gender'].fillna('f')
    df[na_wildcards] = df[na_wildcards].fillna(0)

    return df


def analyze_hospitals(df):
    # hospital with the highest number of patients
    first = df['hospital'].mode()[0]

    # share of stomach-related issues in the general hospital
    general_patients = df[df['hospital'] == 'general']
    second = (general_patients['diagnosis'] == 'stomach').mean()

    # share of dislocation-related issues in the sports hospital
    sports_patients = df[df['hospital'] == 'sports']
    third = (sports_patients['diagnosis'] == 'dislocation').mean()

    # difference in median ages in the general and sports hospitals
    fourth = general_patients['age'].median() - sports_patients['age'].median()

    # hospital with the most blood tests taken
    blood_tests = df[df['blood_test'] == 't'].groupby('hospital').size()
    fifth = blood_tests.idxmax()
    fifth_count = blood_tests.max()
    fifth_result = f'{fifth}, {fifth_count} blood tests'

    return first, second, third, fourth, fifth_result


def fourth_stage():
    first, second, third, fourth, fifth = analyze_hospitals(df)

    print(f'The answer to the 1st question is {first}\n'
          f'The answer to the 2nd question is {second:.3f}\n'
          f'The answer to the 3rd question is {third:.3f}\n'
          f'The answer to the 4th question is {fourth}\n'
          f'The answer to the 5th question is {fifth}')


def analyze_graph(df):
    """
        1) What is the most common age of a patient among all hospitals? Plot a histogram and choose one of the following age ranges: 0-15, 15-35, 35-55, 55-70, or 70-80.
        2) What is the most common diagnosis among patients in all hospitals? Create a pie chart.
        3) Build a violin plot of height distribution by hospitals. Try to answer the questions.
            What is the main reason for the gap in values? Why there are two peaks,
            which correspond to the relatively small and big values? No special form is required
            to answer this question.
    """
    # the most common age of a patient among all hospitals / histogram
    bins = [0, 15, 35, 55, 70, 80]
    counts, bin_edges, _ = plt.hist(df['age'], bins=bins)
    most_common_bin_index = np.argmax(counts)
    start = bin_edges[most_common_bin_index]
    end = bin_edges[most_common_bin_index + 1]
    first_ans = f'{start}-{end}'
    plt.show()

    # the most common diagnosis among patients in all hospitals / pie chart
    diagnosis_counts = df['diagnosis'].value_counts()
    most_common_diagnosis = diagnosis_counts.idxmax()
    plt.pie(diagnosis_counts, labels=diagnosis_counts.index)
    plt.show()

    # violin plot of height
    plt.violinplot(df['height'])
    plt.show()
    third = 'The author of the sports table did everything in freedom units 🦅🦅🦅 The weights are in pounds as well.'

    return first_ans, most_common_diagnosis, third


def fifth_stage():
    first, second, third = analyze_graph(df)
    print(f'The answer to the 1st question: {first}\n'
          f'The answer to the 2nd question: {second}\n'
          f'The answer to the 3rd question: {third}')


if __name__ == '__main__':
    df = load_and_clean_data()
    fifth_stage()

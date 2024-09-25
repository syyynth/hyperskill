import os
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests


def download():
    if not os.path.exists('../Data'):
        os.mkdir('../Data')

    # Download data if it is unavailable.
    if 'Nobel_laureates.json' not in os.listdir('../Data'):
        sys.stderr.write("[INFO] Dataset is loading.\n")
        url = 'https://www.dropbox.com/s/m6ld4vaq2sz3ovd/nobel_laureates.json?dl=1'
        r = requests.get(url, allow_redirects=True)
        with open('../Data/Nobel_laureates.json', 'wb') as f:
            f.write(r.content)
        sys.stderr.write("[INFO] Loaded.\n")


def contains_duplicates(data):
    return data.duplicated().any()


def load(path):
    return pd.read_json(path)


def stage_1(data, show):
    ans1 = contains_duplicates(data)

    data.dropna(subset='gender', inplace=True)
    data.reset_index(drop=True, inplace=True)

    ans2 = data[['country', 'name']].head(20).to_dict()

    if show:
        print(ans1)
        print(ans2)


def extract_country(place_of_birth):
    if not place_of_birth or ',' not in place_of_birth:
        return None
    return place_of_birth.split(',')[-1].strip()


def stage_2(data, show):
    reps = {'US': 'USA', 'United States': 'USA', 'U.S.': 'USA', 'United Kingdom': 'UK'}

    data['born_in'] = (
        data['born_in']
        .replace('', None)
        .fillna(data['place_of_birth'].apply(extract_country))
        .replace(reps)
    )

    data.dropna(subset='born_in', inplace=True)
    data.reset_index(drop=True, inplace=True)

    if show:
        print(data['born_in'].tolist())


def get_year_born(df):
    return df['date_of_birth'].apply(lambda x: pd.to_datetime(x).year)


def age_of_getting_novel(df):
    return df['year'] - df['year_born']


def stage_3(data, show):
    data['year_born'] = get_year_born(data)
    ans1 = data['year_born']

    data['age_of_winning'] = age_of_getting_novel(data)
    ans2 = data['age_of_winning']

    if show:
        print(ans1.values.tolist())
        print(ans2.values.tolist())


def autopct(res):
    return lambda x: f'{x:.2f}%\n({x * res.sum() / 100:.0f})'


def stage_4(data, show):
    if show:
        res = data['born_in'].value_counts()
        other_countries_sum = res[res < 25].sum()
        res = pd.concat([res[res >= 25], pd.Series({'Other countries': other_countries_sum})])

        colors = ['orange', 'red', 'yellow', 'green', 'pink', 'brown', 'cyan', 'purple', 'blue']
        explode = [0.08 if val / res.sum() < 0.1 else 0 for val in res]

        plt.figure(figsize=(12, 12))
        plt.pie(res,
                startangle=135,
                explode=explode,
                labels=res.index,
                colors=colors,
                autopct=autopct(res))
        plt.axis('equal')
        plt.show()


def stage_5(data, show):
    if show:
        pivot_table = data[data['category'] != ''].pivot_table(
            index='category',
            columns='gender',
            values='country',
            aggfunc='count'
        )
        categories = pivot_table.index.tolist()
        female_counts = pivot_table['female'].tolist()
        male_counts = pivot_table['male'].tolist()

        fig, ax = plt.subplots(figsize=(10, 10))

        width = 0.4
        x = np.arange(len(categories))

        ax.bar(x - width / 2, male_counts, width=width, label='Males', color='blue')
        ax.bar(x + width / 2, female_counts, width=width, label='Females', color='crimson')

        plt.title('The total count of male and female Nobel Prize winners by categories', fontsize=20)
        plt.xlabel('Category', fontsize=14)
        plt.xticks(categories)
        plt.ylabel('Nobel Laureates Count', fontsize=14)

        plt.legend(['Males', 'Females'])
        plt.show()


def stage_6(data, show):
    if show:
        table = data[data['category'] != '']
        categories = table['category'].unique().tolist()
        datas = [group['age_of_winning'] for _, group in table.groupby('category')]
        datas.append(table['age_of_winning'])

        plt.figure(figsize=(10, 10))

        # labels is deprecated, `tick_labels` should be used
        plt.boxplot(datas, labels=categories + ['All categories'], showmeans=True)

        plt.ylabel('Age of Obraining the Novel Prize', fontsize=14)
        plt.xlabel('Category', fontsize=14)
        plt.title('Distribution of Ages by Category', fontsize=20)

        plt.show()


def main():
    download()
    data = load('../Data/Nobel_laureates.json')
    stage_1(data, False)
    stage_2(data, False)
    stage_3(data, False)
    stage_4(data, False)
    stage_5(data, False)
    stage_6(data, True)


if __name__ == '__main__':
    main()

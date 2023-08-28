import numpy as np
import pandas as pd


def min_max_norm(df: pd.DataFrame, cols: list[str], min_max=None) -> pd.DataFrame:
    for col in cols:
        col_min = df[col].min() if min_max is None else min_max.loc['min', col]
        col_max = df[col].max() if min_max is None else min_max.loc['max', col]
        df[col] = (df[col] - col_min) / (col_max - col_min)
    return df


def calc_dists(train, test):
    return [[np.linalg.norm(np.r_[u[1:]] - np.r_[v[1:]]) for v in train.itertuples()]
            for u in test.itertuples()]


def k_closest_labels(dist, labels, k):
    return sorted(zip(dist, labels))[:k]


def predict(labels):
    true = sum(dist[1] for dist in labels)
    false = len(labels) - true
    return int(true > false)


def main() -> None:
    train_path = '../Data/data_about_marathon_runners.txt'
    test_path = '../Data/test.txt'
    names = 'y', 'km', 'age', 'time', 'cross'

    hots = {
        'cycling 3h': [1, 0, 0, 0],
        'cycling 4h': [0, 1, 0, 0],
        'cycling 5h': [0, 0, 1, 0],
        'nothing': [0, 0, 0, 1]
    }
    converters = {'cross': lambda x: hots[x], 'y': lambda x: x == 'Yes'}

    df = pd.read_csv(train_path, names=names, converters=converters)
    test_df = pd.read_csv(test_path, names=names[1:], converters=converters)
    info = df.describe()

    df = min_max_norm(df, ['km', 'age'])
    test_df = min_max_norm(test_df, ['km', 'age'], info)

    dists = calc_dists(df.drop(columns='y'), test_df)
    for k in 1, 3, 5:
        y_hat = [predict(k_closest_labels(d, df['y'], k)) for d in dists]
        print(f'Result with k = {k}: {y_hat}')


if __name__ == '__main__':
    main()

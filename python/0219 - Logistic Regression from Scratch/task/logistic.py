import numpy as np
import pandas as pd
from sklearn.datasets import load_breast_cancer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split


def sigmoid(t):
    return 1 / (1 + np.exp(-t))


def exp_or_narrowed(arr):
    # is this what it's asking?
    change1 = abs(min(arr[0]) - max(arr[0]))
    change2 = abs(min(arr[-1]) - max(arr[-1]))
    return 'expanded' if change2 > change1 else 'narrowed'


class CustomLogisticRegression:
    def __init__(self, fit_intercept=True, l_rate=0.01, n_epoch=1000):
        self.coef_ = None
        self.errors = None
        self.fit_intercept = fit_intercept
        self.l_rate = l_rate
        self.n_epoch = n_epoch

    def predict_proba(self, row, coef_):
        bias, *w = coef_
        return sigmoid(self.fit_intercept * bias + row @ w)

    def fit(self, X, y, loss='ll'):
        if self.fit_intercept:
            X = np.c_[np.ones(X.shape[0]), X]

        self.coef_ = np.zeros(X.shape[1])
        self.errors = []

        # changed it from batch to stochastic, so it matches graphs :)
        for _ in range(self.n_epoch):
            stochastic_err = []
            for i in range(X.shape[0]):
                y_hat = sigmoid(X[i] @ self.coef_)

                if loss == 'mse':
                    err = (y[i] - y_hat) ** 2
                    gradient = (y_hat - y[i]) * y_hat * (1 - y_hat)
                elif loss == 'll':
                    err = -(y[i] * np.log(y_hat) + (1 - y[i]) * np.log(1 - y_hat))
                    gradient = (y_hat - y[i]) / X.shape[0]

                stochastic_err.append(err / X.shape[0])
                self.coef_ -= self.l_rate * X[i] * gradient

            self.errors.append(stochastic_err)

    def predict(self, X, cut_off=0.5):
        if self.fit_intercept:
            X = np.c_[np.ones(X.shape[0]), X]

        y_pred = sigmoid(X @ self.coef_)
        return [0 if y <= cut_off else 1 for y in y_pred]


def main():
    f_names = ['worst concave points', 'worst perimeter', 'worst radius']

    breast_cancer = load_breast_cancer()

    X = pd.DataFrame(data=breast_cancer.data, columns=breast_cancer.feature_names)[f_names]
    X = X.apply(lambda x: (x - x.mean()) / x.std())
    y = breast_cancer.target

    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.8, random_state=43)

    clf = CustomLogisticRegression()
    clf.fit(X_train, y_train, 'mse')
    acc_mse = accuracy_score(y_test, clf.predict(X_test))
    err_mse = clf.errors

    clf.fit(X_train, y_train)
    acc_ll = accuracy_score(y_test, clf.predict(X_test))
    err_ll = clf.errors

    clf_sk = LogisticRegression()
    clf_sk.fit(X_train, y_train)
    acc_sk = accuracy_score(y_test, clf_sk.predict(X_test))

    ans = {'mse_accuracy': acc_mse, 'logloss_accuracy': acc_ll, 'sklearn_accuracy': acc_sk,
           'mse_error_first': err_mse[0], 'mse_error_last': err_mse[-1],
           'logloss_error_first': err_ll[0], 'logloss_error_last': err_ll[-1]}
    print(ans)

    ans2 = f"""Answers to the questions:
            1) {min(err_mse[0]):.5f}
            2) {min(err_mse[-1]):.5f}
            3) {max(err_ll[0]):.5f}
            4) {max(err_ll[-1]):.5f}
            5) {exp_or_narrowed(err_mse)}
            6) {exp_or_narrowed(err_ll)}"""
    print(ans2)


if __name__ == '__main__':
    main()

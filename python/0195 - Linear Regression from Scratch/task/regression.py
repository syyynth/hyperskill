import numpy as np
from sklearn.linear_model import LinearRegression as LR
from sklearn.metrics import mean_squared_error, r2_score


class LinearRegression:
    def __init__(self, *, fit_intercept=True):
        self.fit_intercept = fit_intercept
        self.coefficient = None
        self.intercept = None

    def add_intercept(self, X):
        return np.c_[np.ones(len(X)) if self.fit_intercept else np.zeros(len(X)), X]

    def fit(self, X, y):
        X = self.add_intercept(X)
        self.intercept, *self.coefficient = np.linalg.pinv(X) @ y

    def predict(self, X):
        X = self.add_intercept(X)
        return X @ np.r_[self.intercept, self.coefficient]

    def r2_score(self, y, yhat):
        return 1 - np.sum((y - yhat) ** 2) / np.sum((y - np.mean(y)) ** 2)

    def rmse(self, y, yhat):
        return np.sqrt(np.mean((y - yhat) ** 2))


f1 = [2.31, 7.07, 7.07, 2.18, 2.18, 2.18, 7.87, 7.87, 7.87, 7.87]
f2 = [65.2, 78.9, 61.1, 45.8, 54.2, 58.7, 96.1, 100.0, 85.9, 94.3]
f3 = [15.3, 17.8, 17.8, 18.7, 18.7, 18.7, 15.2, 15.2, 15.2, 15.2]
y = [24.0, 21.6, 34.7, 33.4, 36.2, 28.7, 27.1, 16.5, 18.9, 15.0]

X = np.c_[f1, f2, f3]

model = LinearRegression()
model.fit(X, y)
y_predict = model.predict(X)

sklearn_lr = LR()
sklearn_lr.fit(X, y)
sklearn_y_predict = model.predict(X)

print({
    'Intercept': model.intercept - sklearn_lr.intercept_,
    'Coefficient': np.r_[model.coefficient] - sklearn_lr.coef_,
    'R2': model.r2_score(y, y_predict) - r2_score(y, sklearn_y_predict),
    'RMSE': model.rmse(y, y_predict) - np.sqrt(mean_squared_error(y, sklearn_y_predict))
})

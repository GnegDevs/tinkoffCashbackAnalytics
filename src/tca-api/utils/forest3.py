import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV

import datetime

from sklearn.ensemble import RandomForestRegressor


def Generateplot(name, budget):
    df = pd.read_csv(f"tca-api/database/{name}_plot.csv", parse_dates=['date'])
    df = df.loc[df["merchant_name"] == name]

    j = pd.Series(pd.date_range(df["date"].min(), df["date"].max()))
    j = j.loc[j.isin(df["date"])]
    start =  df["date"].min()
    print(start)
    print(df)
    print(j)
    df["datecount"] = j.index

    X = df["datecount"]
    y = df["cashback"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
    X_train = np.array(X_train).reshape((-1, 1))
    y_train = np.array(y_train).reshape((-1, 1))
    X_test = np.array(X_test).reshape((-1, 1))
    y_test = np.array(y_test).reshape((-1, 1))

    print(X_train, y_train)
    rf_regressor = RandomForestRegressor(n_estimators=100, random_state=0)
    rf_regressor.fit(X_train, y_train)

    y_pred_train = rf_regressor.predict(X_train)
    r2_score(y_train, y_pred_train)

    """fig, ax = plt.subplots()
    ax.scatter(X_train, y_train, color="red")
    ax.scatter(X_train, y_pred_train, color="blue")
    plt.show()"""
    y_pred = rf_regressor.predict(X_test)
    r2_score(y_test, y_pred)

    """fig, ax = plt.subplots()
    ax.scatter(X_test, y_test, color="red")
    ax.scatter(X_test, y_pred, color="blue")
    plt.show()"""

    param_grid = {
        'bootstrap': [True],
        'max_depth': [100, 100, 50, None],
        'max_features': ["sqrt", "log2", None],
        'min_samples_leaf': [1, 3, 5],
        'min_samples_split': [2, 3, 4],
        'n_estimators': [10, 25, 50, 75, 100]
    }

    rf = RandomForestRegressor()
    grid_search = GridSearchCV(estimator=rf, param_grid=param_grid, cv=4, verbose=2, scoring='r2', n_jobs=-1)
    grid_search.fit(X_train, y_train)

    y_pred = grid_search.predict(X_train)
    print((r2_score(y_train, y_pred)))
    y_pred = grid_search.predict(X_test)
    print(r2_score(y_test, y_pred))
    """fig, ax = plt.subplots()
    x_ax = range(len(y_test))
    plt.plot(x_ax, y_test, linewidth=1, label="original")
    plt.plot(x_ax, y_pred, linewidth=1.1, label="predicted")
    plt.title("y-test and y-predicted data")
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.legend(loc='best', fancybox=True, shadow=True)
    plt.grid(True)"""

    datenum = df["datecount"].min()
    itog = pd.DataFrame(columns=["date", "cashback"])
    date = start
    plt.show()
    itdate = df["date"].max()
    while itog["cashback"].sum() < budget:
        y = grid_search.predict(np.array(range(datenum, datenum + 5)).reshape((-1, 1)))
        x = pd.date_range(date, date + datetime.timedelta(4)).tolist()
        itdate = date
        itog = pd.concat([itog, pd.DataFrame({"date": x, "cashback": y})], ignore_index=True)
        date = date + datetime.timedelta(5)
        datenum += 5

    ax = plt.subplots()
    itog.plot(x="date", y="cashback", color="black")

    plt.show()

    plt.savefig(f'{name}_plot.png')
    return itdate, budget - itog["cashback"][:-5].sum()

print(Generateplot("Перекресток", 10000000000))
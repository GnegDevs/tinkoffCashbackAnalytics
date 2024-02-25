import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV
 
from datetime import date as dt
from datetime import timedelta

from sklearn.ensemble import RandomForestRegressor

from utils.generateCSV import *

def generatePlot(name):
    # generateCSV(name)


    df = pd.read_csv(f"tca-api/database/{name}_plot.csv",parse_dates=['date'])
    budget = 10000
    date = dt(2022, 3, 31)
    print(pd.date_range(date, date + timedelta(5)).tolist())

    """cashback =
    name =

    df[len(df)] = [name, cashback, date]"""

    df = df.loc[df["merchant_name"] == name]
    print(df)
    j = pd.Series(pd.date_range(df["date"].min(), df["date"].max()))
    j = j.loc[j.isin(df["date"])]
    l = list(map(int, df["date"].min().split("-")))
    start = datetime.date(*l)
    print(start)
    df["datecount"] = j.index

    X = df["datecount"]
    y = df["cashback"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)
    X_train = np.array(X_train).reshape((-1, 1))
    y_train = np.array(y_train).reshape((-1, 1))
    X_test = np.array(X_test).reshape((-1, 1))
    y_test = np.array(y_test).reshape((-1, 1))

    print(X_train, y_train)
    rf_regressor = RandomForestRegressor(n_estimators = 10, random_state = 0)
    rf_regressor.fit(X_train, y_train)

    y_pred_train = rf_regressor.predict(X_train)
    r2_score(y_train, y_pred_train)

    fig, ax = plt.subplots()
    ax.plot(X_train,y_train, color = "red")
    ax.plot(X_train,y_pred_train, color = "blue")
    plt.show()
    y_pred = rf_regressor.predict(X_test)
    r2_score(y_test, y_pred)

    fig, ax = plt.subplots()
    ax.plot(X_test,y_test, color = "red")
    ax.plot(X_test,y_pred, color = "blue")
    plt.show()

    param_grid = {
        'bootstrap': [True],
        'max_depth': [80, 90, 100, None],
        'max_features': ["sqrt", "log2", None],
        'min_samples_leaf': [1, 3, 5],
        'min_samples_split': [2, 3, 4],
        'n_estimators': [10, 25, 50, 75, 100]
    }

    rf = RandomForestRegressor()
    grid_search = GridSearchCV(estimator = rf, param_grid = param_grid, cv = 5, verbose =2, scoring='r2', n_jobs = -1)
    grid_search.fit(X_train, y_train)


    y_pred =grid_search.predict(X_train)
    print((r2_score(y_train, y_pred)))
    y_pred = grid_search.predict(X_test)
    print(r2_score(y_test, y_pred))
    fig, ax = plt.subplots()
    x_ax = range(len(y_test))
    plt.plot(x_ax, y_test, linewidth=1, label="original")
    plt.plot(x_ax, y_pred, linewidth=1.1, label="predicted")
    plt.title("y-test and y-predicted data")
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.legend(loc='best',fancybox=True, shadow=True)
    plt.grid(True)


    datenum = (date - start).days
    datenum = 4
    itog = pd.DataFrame(columns=["date", "cashback"])

    na = 0
    while itog["cashback"].sum()<budget:
        y = grid_search.predict(np.array(range(datenum, datenum+5)).reshape((-1, 1)))
        x = pd.date_range(date, date + datetime.timedelta(4)).tolist()
        print(y)
        itog= pd.concat([itog, pd.DataFrame({"date":x, "cashback":y})], ignore_index=True)
        date = date + datetime.timedelta(5)
        datenum += 5
        na += 5

    itog["cashback"].plot()

    plt.show()

generatePlot("Перекресток")
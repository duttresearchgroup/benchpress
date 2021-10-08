from typing import List
import pandas as pd
import requests
import os
import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score

def main():
    metric_name = ['Application','Frequency']
    # Load the diabetes dataset
    diabetes_X, diabetes_y = datasets.load_diabetes(return_X_y=True)
    df_power = pd.read_csv("data_d.csv")
    df_freq = pd.read_csv("Jaeger.csv")
    power_list, freq_list = [], []
    for timestamp in df_freq['Time']:
        temp_row_power = df_power.loc[df_power['Time'] == timestamp]
        temp_row_freq = df_freq.loc[df_freq['Time'] == timestamp]
        # print(temp_row_power['node_tplink_power'])
        power_list.append(temp_row_power['node_tplink_power'].item())
        freq_list.append(temp_row_freq['Frequency'].item())
    # print(freq_list)
        # temp_row_freq = df_freq.loc[(df_freq['Time'] == timestamp)]

    nparray_x = np.array(freq_list).reshape(-1,1)
    nparray_y = np.array(power_list)

    print(nparray_x)
    print(nparray_y)
    # print(len(nparray_y))
    y_train = nparray_y[:-50]
    y_test = nparray_y[-50:]

    x_train = nparray_x[:-50]
    x_test = nparray_x[-50:]
    # print(type(nparray_x))
    regr = linear_model.LinearRegression()
    regr.fit(x_train, y_train)
    y_pred = regr.predict(x_test)

#     # Plot outputs
    plt.scatter(x_test, y_test,  color='black')
    plt.plot(x_test, y_pred, color='blue', linewidth=3)

    plt.xticks(())
    plt.yticks(())

    plt.show()

if __name__ == "__main__":
    main()
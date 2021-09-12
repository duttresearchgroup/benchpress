from types import coroutine
from typing import Collection
from numpy import mean
from numpy import std
from numpy.core.fromnumeric import size
from numpy.random import randn
from numpy.random import seed
import pandas as pd
from pandas.core.algorithms import value_counts
from pandas.io.pytables import Fixed

fixed_var = ["node_tplink_power","node_rapl_core_joules_total","node_rapl_dram_joules_total","node_rapl_package_joules_total"]
# fixed_var = ["node_rapl_core_joules_total"]
threhold = 0
def find_corr():
    
    df = pd.read_csv('data.csv')
    df = df.drop([df.columns[0],"Time"], axis = 1)
    corr_matrix = df.corr()
    filterred_corr_matrix = corr_matrix.filter(items=fixed_var, axis=0).fillna(0)
    corr_metrics = []
    for key in filterred_corr_matrix.columns:
        
        if key in fixed_var:
            continue
        if key.startswith('go'):
            continue
        
        isCorr = True
        for row in fixed_var:
            if filterred_corr_matrix[key][row] < threhold:
                isCorr = False
                break
        if (isCorr):
            print(filterred_corr_matrix[key])
            corr_metrics.append(key)
    # print (corr_metrics)
def main():
    find_corr()

if __name__ == "__main__":
    main()

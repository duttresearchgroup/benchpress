from types import coroutine
from typing import Collection
from numpy import mean
from numpy import std
from numpy.core.fromnumeric import size
from numpy.random import randn
from numpy.random import seed
import pandas as pd
from pandas.core.algorithms import rank, value_counts
from pandas.io.pytables import Fixed
import operator
import sys

fixed_var = ["node_tplink_power","node_rapl_core_joules_total","node_rapl_dram_joules_total","node_rapl_package_joules_total"]
# fixed_var = ["node_rapl_core_joules_total"]
threhold = 0
def find_corr():
    
    df = pd.read_csv(sys.argv[1])
    df = df.drop([df.columns[0],"Time"], axis = 1)
    corr_matrix = df.corr()
    filterred_corr_matrix = corr_matrix.filter(items=fixed_var, axis=0).fillna(0)
    corr_metrics = []
    rank = {}
    for key in filterred_corr_matrix.columns:
        
        # if key in fixed_var:
        #     continue
        if key.startswith('go'):
            continue
        
        isCorr = True
        for row in fixed_var:
            if filterred_corr_matrix[key][row] < threhold:
                isCorr = False
                break
            if(row =="node_tplink_power" and filterred_corr_matrix[key][row]>0.5):
                rank[str(key)] = float(filterred_corr_matrix[key][row])
        if (isCorr):
            # print(filterred_corr_matrix[key])
            corr_metrics.append(key)
    
    #sorted parameter list 
    sorted_list = sorted(rank.items(),key=lambda item:item[1],reverse=True)
    for i in range(len(sorted_list)):
        print(sorted_list[i],'\n')
def main():
    find_corr()

if __name__ == "__main__":
    main()

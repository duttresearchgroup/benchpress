from typing import Collection
from numpy import mean
from numpy import std
from numpy.core.fromnumeric import size
from numpy.random import randn
from numpy.random import seed
from matplotlib import pyplot
import pandas as pd
from pandas.core.algorithms import value_counts
import seaborn as sn

parameter_list = ["node_tplink_power","node_rapl_core_joules_total","node_rapl_dram_joules_total","go_memstats_mspan_inuse_bytes"]
data_label = ["tplink_power","core_joules","dram_joules","mspan_inuse_bytes"]
count, j,k=0,0,0
data_merge=[]

with open('data.csv','r') as inputfile:
    rows = [line.split(',') for line in inputfile.readlines()]
    
    data = [line[1:-1] for line in rows if line[0] == parameter_list[0]]
    
    hashmap={}
    for i in range(0,4):
        data = [line[1:-1] for line in rows if line[0] == parameter_list[i]]
        j=0
        data_merge=[]
        while j < len(data[0]):
            
            value=data[0][j+1].replace(']"','').replace("'",'"').replace(" ","").replace('"','')
            data_merge.append(value)
            j+=2
        hashmap[data_label[k]] = data_merge
        k += 1
        df = pd.DataFrame(data=hashmap,columns=data_label)
df_flo=df.astype(float)
corr_matrix = df_flo.corr()
print(corr_matrix)
sn.heatmap(corr_matrix, annot=True)
pyplot.show()
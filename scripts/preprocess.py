import os
os.chdir('outdir') 
import pandas as pd
import glob
import re
import sys


files = glob.glob('*turbo*.log')

df=pd.DataFrame()

for i in files:

    file_name = open(i).read()
    s=[float(s) for s in re.findall(r'-?\d+\.?\d*', file_name)]
    con1=s[5]
    con2=s[6]
    ins=s[7]*1000000000+s[8]*1000000+s[9]*1000+s[10]
    time=s[11]
    a=[float(s) for s in re.findall(r'-?\d+\.?\d*', i)]
   # if (i.split("_")[0]=="fio"):
    #    testName="aio"
   # else:
   #     testName="default" 

    data = {'power/energy-cores/':[con1],
            'power/energy-pkg/':[con2],
            'instructions':[ins],
            'time':[time],
            'Appname' :[sys.argv[3]],
            'iteration':[a[1]],
            'Turbo Mode' :[a[0]],
            'Test Name':[sys.argv[4]]

            }

    df1 = pd.DataFrame(data, columns = ['Appname','Test Name','Turbo Mode','iteration','power/energy-cores/','power/energy-pkg/','instructions','time'])
    df = pd.concat([df,df1])

  


df.to_csv(sys.argv[2], index=False) 

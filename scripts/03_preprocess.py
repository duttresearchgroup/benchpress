import os
import pandas as pd
import glob
import re
import sys

# Defining main function
def main():
    
    df=pd.DataFrame()
    for root, _, files in os.walk(sys.argv[1], topdown=False):
        for name in files:
            # Filter perf logs
            if ("perf" in name):
                print("Parsing: ", os.path.join(root, name))
                app_delimiter = name.index('_')
                app_name  = (name[:app_delimiter])
                # test_name = (name[app_delimiter+1:name.index('_', app_delimiter+1)])
                file = open(os.path.join(root, name), "r")
                for line in file:
                    if re.search("energy-cores", line):
                        metric_energy_cores=re.findall("\d+\.\d+", line)[0]
                    elif re.search("energy-pkg", line):
                        metric_energy_pkg=re.findall("\d+\.\d+", line)[0]
                    elif re.search("instructions", line):
                        line = line.replace(',', '')
                        ins=re.findall("\d+", line)[0]
                    elif re.search("time", line):
                        time=re.findall("\d+\.\d+", line)[0]

                a=[int(s) for s in re.findall(r'-?\d', name)]
                data = {'power/energy-cores/':[metric_energy_cores],
                        'power/energy-pkg/':[metric_energy_pkg],
                        'instructions':[ins],
                        'time':[time],
                        'Appname' :[app_name],
                        'iteration':[a[1]],
                        'Turbo Mode' :[a[0]]
                        }

                df_tmp = pd.DataFrame(data, columns = ['Appname', 'Turbo Mode','iteration','power/energy-cores/','power/energy-pkg/','instructions','time'])
                df = pd.concat([df,df_tmp])

    df.to_csv(sys.argv[2], index=False) 

# __name__
if __name__=="__main__":
    if (len(sys.argv)<3):
        print ('Required params:', sys.argv[0], '<directory with log files> <output filename>')
    else:
        main()

from os import stat_result
import pandas as pd
from pandas.core.indexes.base import Index
import requests
import sys
import os.path
import datetime
import argparse

# For all the fields in this list, create a separate column
# Example: node_disk_discard_time_seconds_total{device="sda"} -> node_disk_discard_time_seconds_total__device_sda
split_list = [ 'mode' ,  'device', ]

# For all the fields in this list, create an average of all values for each timestamp
# Example: node_cpu_frequency_max_hertz{cpu="0"} + {cpu="1"} + .. {cpu="5"} / 6
avg_list = [ 'cpu' ]


parser = argparse.ArgumentParser(description='Get data from Prometheus Server')

def getLabelNames(url):
    response = requests.get('{0}/api/v1/label/__name__/values'.format(url))
    print("Fetching timeseries keys")
    # print(response.request.url)
    names = response.json()['data']    #Return matrix names
    return names

def getArguments():
    parser.add_argument('-l', '--url',
                        action='store',
                        type=str,
                        )
    parser.add_argument('-f', '--filename',
                        action='store',
                        type=str,
                        )
    parser.add_argument('--step',
                        action='store',
                        type=int,
                        )
    args = parser.parse_args()
    return args

def writeToCSV(args):
    my_file = open("traces_test.txt","r")
    my_traces = my_file.readlines()

    for i in range(len(my_traces)):
        start = my_traces[i].find("from=")+5
        mid = my_traces[i].find("&to=")
        end = my_traces[i].find("\n")

        start_unix = my_traces[i][start:mid-3]
        end_unix   = my_traces[i][mid+4:end-3]
        merged_data = pd.DataFrame()
        print(start_unix)
        print(end_unix)
        # metricNames = ["node_cpu_frequency_max_hertz", "node_cpu_guest_seconds_total"]
        # metricNames = ["node_tplink_power","node_rapl_core_joules_total", "network_address_assign_type"]
        # metricNames = ["node_rapl_core_joules_total","node_cpu_scaling_frequency_hertz"]
        
        metricNames=getLabelNames(args.url)

        for metricName in metricNames:
            # *****************************************************
            response = requests.get('{0}/api/v1/query_range'.format(args.url), params={'query': metricName,'start': start_unix, 'end': end_unix,'step': args.step})
            # print(response.request.url)
            flag = 0
            results = response.json()['data']['result']
            
            # # Special case 2: Split
            
            for metric in split_list:
                # print(results[0])
                if (metric in results[0]['metric']):
                    for i in range(len(results)):
                        results[i]['metric']['__name__']= str(results[i]['metric']['__name__'])+'_'+metric+'_'+str(results[i]['metric'][metric])
            #  # Special case 1: Average
            for metric in avg_list:
                if (metric in results[0]['metric']):
                
                    # df_per_cpu[len(results)] -> Each result is a pandas dataframe
                    # df_average = avg(df_per_cpu) -> Take average by timestamp

                    average_df = pd.DataFrame()
                    for k in range(int(len(results)/12)):
                        avg_df_list=[]
                        for j in range(len(results[0]['values'])):
                            sum,avg = 0, 0
                            for i in range(len(results)):
                                sum += float(results[i]['values'][j][1])
                            avg = sum/(len(results))
                            avg_df_list.append(avg)
                            # print(avg_df_list)
                            col_name = str(results[k]['metric']['__name__'])
                        merged_data[col_name] = avg_df_list
                    flag = 1
                        
                    # frames = [merged_data,average_df]
                    # result = pd.concat(frames)    
            #         # ******************************
                    # print("!!", metric)
            #         # ******************************
            for timeseries in results:
                if flag ==1:
                    break
                if 'Time' not in merged_data:
                    df_time = [value[0] for value in timeseries['values']]
                    merged_data['Time'] = df_time
                
            for timeseries in results:
                metric_name = timeseries['metric']['__name__']
                df_value = [value[1] for value in timeseries['values']]
                if flag ==1:
                    break
            
                if ( len(merged_data['Time']) == len(df_value)):
                    merged_data[metric_name] = df_value
                else:
                    print("[Warning] ", metric_name, " skipped.")
            # *****************************************************
        if(os.path.isfile(args.filename)):
            merged_data.to_csv(args.filename, mode='a',header=False,index=False)
        else:
            merged_data.to_csv(args.filename,index=False)
        # merged_data.to_csv(args.filename)
        print("-----------------------------------------------------------------------------------------------------------------------------")

def main():
    args = getArguments()
 
    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(1)
    
    writeToCSV(args)

if __name__ == "__main__":
    main()
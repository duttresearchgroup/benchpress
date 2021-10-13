import threading
import pandas as pd
from pandas.core.indexes.base import Index
from collections import OrderedDict
import requests
import sys
import os.path
import argparse
from urllib.parse import urlparse, parse_qs
import asyncio
import aiohttp
import numpy as np

# For all the fields in this list, create a separate column
# Example: node_disk_discard_time_seconds_total{device="sda"} -> node_disk_discard_time_seconds_total__device_sda
split_list = [ 'mode' ,  'device', ]

# For all the fields in this list, create an average of all values for each timestamp
# Example: node_cpu_frequency_max_hertz{cpu="0"} + {cpu="1"} + .. {cpu="5"} / 6
avg_list = [ 'cpu' ]

metric_name_jaeger = ['Application','Frequency']

grafana_links_filename = "G_links_10_08.txt"
jaeger_links_filename = "J_links_10_08.txt"

parser = argparse.ArgumentParser(description='Get data from Prometheus Server')

# getting the metric labels from Prometheus
def getLabelNames(url):
    response = requests.get('{0}/api/v1/label/__name__/values'.format(url))
    # print("Fetching timeseries keys")
    print(response.request.url)
    names = response.json()['data']    #Return matrix names
    return names
# input parser
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
# write the query data from Prometheus and Jaeger into a csv file

async def query_from_prometheus_jaeger(args,prometheus_traces,jaeger_links):
    for link_index in range(len(prometheus_traces)):
        # print("'", prometheus_traces[link_index], "'")
        parsed_url = urlparse(prometheus_traces[link_index])
        start_unix = parse_qs(parsed_url.query)['from'][0][0:10] 
        end_unix   = parse_qs(parsed_url.query)['to'][0][0:10]

        merged_data_prometheus = pd.DataFrame()
        # metricNames = ["node_cpu_frequency_max_hertz", "node_cpu_guest_seconds_total"]
        # metricNames = ["node_tplink_power","node_rapl_core_joules_total", "network_address_assign_type"]
        # metricNames = ["node_rapl_core_joules_total","node_cpu_scaling_frequency_hertz"]
        # metricNames = ["node_perf_branch_instructions_total","node_perf_branch_instructions_total","node_perf_int_misc_recovery_cycles_any"]
        metricNames=getLabelNames(args.url)

        async with aiohttp.ClientSession() as session:
            for metricName in metricNames:
            
                params = OrderedDict([('query', metricName), ('start', start_unix), ('end', end_unix), ('step', args.step)])
                response = await asyncio.create_task(session.get('{0}/api/v1/query_range'.format(args.url), params=(params),ssl=False))
                
                flag = 0
                # print(response.json())
                holder = await response.json()
                results = holder['data']['result']
                # Special case 1: Split
                # Extend label name if it satisfies   
                if (len(results)==0):
                    continue
                for metric in split_list:
                    # print(results[0])
                    if (metric in results[0]['metric']):
                        for i in range(len(results)):
                            results[i]['metric']['__name__']= str(results[i]['metric']['__name__'])+'_'+metric+'_'+str(results[i]['metric'][metric])
                #  # Special case 2: Average
                for metric in avg_list:
                    if (metric in results[0]['metric']):
                    
                        # df_per_cpu[len(results)] -> Each result is a pandas dataframe
                        # df_average = avg(df_per_cpu) -> Take average by timestamp

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
                            merged_data_prometheus[col_name] = avg_df_list
                        flag = 1
                # Start writing the Prometheus dataframe
                # Put Time in the first column  
                for timeseries in results:
                    if flag ==1:
                        break
                    if 'Time' not in merged_data_prometheus:
                        df_time = [value[0] for value in timeseries['values']]
                        merged_data_prometheus['Time'] = df_time

                for timeseries in results:
                    metric_name = timeseries['metric']['__name__']
                    df_value = [value[1] for value in timeseries['values']]
                    if flag ==1:
                        break
                
                    if ( len(merged_data_prometheus['Time']) == len(df_value)):
                        merged_data_prometheus[metric_name] = df_value
                    else:
                        print("[Warning] ", metric_name, " skipped.")
        # ****************************************
        # Query from Jaeger
        # ****************************************
        async with aiohttp.ClientSession() as session1:
            response_jae = await asyncio.create_task(session1.get(jaeger_links[link_index],ssl=False))
            holder2 =  await response_jae.json()
            results_jae = holder2["data"]
            tags = results_jae[0]['spans'][0]['tags'] 
            # merged_data_jaeger = pd.DataFrame()
            # going through the tags to find the desired ones
            for tag in tags:
                if tag['key'] in metric_name_jaeger:
                    # hold=[]
                    # hold.append(tag['value'])
                    # merged_data_jaeger[tag['key']]= hold
                    merged_data_prometheus[tag['key']] = tag['value']
        # ****************************************
        # Query from Jaeger ends
        # ****************************************
        if(os.path.isfile(args.filename)):
            merged_data_prometheus.to_csv(args.filename, mode='a',header=False,index=False)
        else:
            merged_data_prometheus.to_csv(args.filename,index=False)

def execute_async(args,prometheus_traces,jaeger_links):      
       asyncio.run(query_from_prometheus_jaeger(args,prometheus_traces,jaeger_links))


# Main function 
def main():
    global p_traces, j_traces
    args_ = getArguments()
    p_traces = open(grafana_links_filename).read().splitlines()
    j_traces = open(jaeger_links_filename).read().splitlines()
    num_thread = os.cpu_count()
    #check the argument length
    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(1)
    # task1 = loop.create_task(query_from_prometheus_jaeger(args))
    # await asyncio.wait([task1])
    # task2 = loop.create_task(query_from_jaeger(args))
    # await asyncio.wait([task2])
    # await asyncio.wait([task1,task2])
    prometheus_splits = np.array_split(p_traces,num_thread)
    jaeger_splits = np.array_split(j_traces,num_thread)
    threads=[]
    for i in range(0,num_thread):
        threads.append(threading.Thread(target=execute_async, args=(args_,prometheus_splits[i],jaeger_splits[i],)))
    [t.start() for t in threads]
    [t.join() for t in threads]
    # asyncio.run(query_from_jaeger(args))
    

if __name__ == "__main__":
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(main())
    # loop.close()
    main()
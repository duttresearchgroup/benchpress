import csv
import requests
import sys

import datetime
import argparse
def GetMetrixNames(url):
    response = requests.get('{0}/api/v1/label/__name__/values'.format(url))
    names = response.json()['data']    #Return metrix names
    return names

print(sys.argv[2])
# added 
parser = argparse.ArgumentParser(description='N/A')
parser.add_argument('-l', '--url',
                    action='store',
                    type=str,
                    )
parser.add_argument('-f', '--filename',
                    action='store',
                    type=str,
                    )
parser.add_argument('-n', '--namespace',
                    action='store',
                    type=str,
                    default='default',
                    )
parser.add_argument('--interval',
                    action='store',
                    type=str,
                    default='5m',
                    )
parser.add_argument('--start',
                    action='store',
                    type=str,
                    )
parser.add_argument('--end',
                    action='store',
                    type=str,
                   )
parser.add_argument('--step',
                    action='store',
                    type=int,
                    )
args = parser.parse_args()
filepath = args.filename
namespace = args.namespace
interval = args.interval
step = args.step

start_str = args.start
end_str = args.end
start_dt = datetime.datetime.strptime(start_str, '%Y%m%d-%H%M')
end_dt = datetime.datetime.strptime(end_str, '%Y%m%d-%H%M')
start_unix = start_dt.timestamp()
end_unix = end_dt.timestamp()

with open('data.csv','w',newline='') as csvFile:
    writer = csv.writer(csvFile)
# writer = csv.writer(sys.stdout)

    if len(sys.argv) < 2:
        print('Usage: {0} http://localhost:9090'.format(sys.argv[0]))
        sys.exit(1)
    metrixNames=GetMetrixNames(sys.argv[2])

    writeHeader=True
    for metrixName in metrixNames:

        #now its hardcoded for hourly
        # response = requests.get('{0}/api/v1/query'.format(sys.argv[2]), params = {'start': start_unix, 'end': end_unix,'step': step})
        response = requests.get('{0}/api/v1/query'.format(sys.argv[2]), params={'query': metrixName,'start': start_unix, 'end': end_unix,'step': step})
        results = response.json()['data']['result']
        # Build a list of all labelnames used.
        #gets all keys and discard __name__
        labelnames = set()
        for result in results:
            labelnames.update(result['metric'].keys())
        # Canonicalize
        labelnames.discard('__name__')
        labelnames = sorted(labelnames)
        # Write the samples.
        if writeHeader:
        #   writer.writerow(['name', 'timestamp', 'value'] + labelnames)
            writeHeader=False
        for result in results:
            l = [result['metric'].get('__name__', '')] + result['values']
            for label in labelnames:
                l.append(result['metric'].get(label, ''))
                writer.writerow(l)
    csvFile.close()


# -------------------------------------------------------------------------------------------------------------------------


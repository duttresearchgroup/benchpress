#!/bin/bash

rm -rf data_d.csv
time python3.8 fetch_data.py -l http://deep.ics.uci.edu:9090 -f data_d.csv --step 1

# FILENAME="log_1.txt"
# cat $FILENAME | grep Grafana > log_2.txt

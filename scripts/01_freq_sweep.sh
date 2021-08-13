#!/bin/bash
# Collect data from monitoring CPU consumption and MIPS while running application

# sudo sh -c 'echo -1 >/proc/sys/kernel/perf_event_paranoid'
# ****************************************************************
# Configuration params
# ****************************************************************
output_folder_name=outdir
iterations=2

# Todo:  Make it work for all the apps
# declare -a  apps=("fio" "schbench" "nginx_wrk_bench" "minebench_plsa")
# declare -a tests=("aio" "default" "default" "default")

declare -a  apps=("fio")
declare -a tests=("aio")
declare -a turbos=("1" "0")
# ****************************************************************

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
rm -rf $output_folder_name
mkdir $output_folder_name

for app_index in "${!apps[@]}";
do 
for turbo in "${turbos[@]}" 
do
    echo -n "no_turbo: " 
    echo $turbo | sudo tee /sys/devices/system/cpu/intel_pstate/no_turbo

    exec_output=$(perf stat --all-cpus --repeat $iterations -e power/energy-cores/ \
    -e power/energy-pkg/ \
    -e instructions \
    -o $output_folder_name/${apps[$app_index]}_no_turbo_$turbo.perf.log \
    python 02_launcher.py ${apps[$app_index]} ${tests[$app_index]} no_turbo $turbo)

    echo $exec_output >> $output_folder_name/${apps[$app_index]}_$iter.log
    
    # docker-compose -f $SCRIPT_DIR/../docker-compose.yml run benchpress python3 benchpress_cli.py -b benchmarks.yml -j jobs/jobs.yml run "${apps[$app_index]} ${tests[$app_index]}"
done
done

# python preprocess.py $output_folder_name output.csv

#rsync -avx jalen@deep.ics.uci.edu:/extradata/guest_users/jalen/file/benchpress/Con_IPS .

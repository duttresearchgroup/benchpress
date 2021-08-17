#!/bin/bash
# Collect data from monitoring CPU consumption and MIPS while running application

# sudo sh -c 'echo -1 >/proc/sys/kernel/perf_event_paranoid'
# ****************************************************************
# Configuration params
# ****************************************************************
output_folder_name=outdir
iterations=1

# Todo:  Make it work for all the apps
declare -a  apps=("fio" "schbench" "nginx_wrk_bench" "minebench_plsa")
declare -a tests=("aio" "default" "default" "default")

# declare -a  apps=("minebench_plsa")
# declare -a tests=("default")
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
    isTurbo="$((1-turbo))"
    
    for iter in $(seq 1 $iterations);
    do 
        exec_output=$(perf stat --all-cpus --repeat 1 -e power/energy-cores/ \
        -e power/energy-pkg/ \
        -e instructions \
        -o $output_folder_name/${apps[$app_index]}_turbo_$isTurbo.perf_ite$iter.log \
        python 02_launcher.py ${apps[$app_index]} ${tests[$app_index]} turbo $isTurbo)

        echo $exec_output > $output_folder_name/${apps[$app_index]}_turbo_${isTurbo}_ite${iter}.log
    done
    # docker-compose -f $SCRIPT_DIR/../docker-compose.yml run benchpress python3 benchpress_cli.py -b benchmarks.yml -j jobs/jobs.yml run "${apps[$app_index]} ${tests[$app_index]}"
done
done

python 03_preprocess.py $output_folder_name output.csv
# Profiling Benchpress benchmarks
We are using a docker container based runtime for running the benchpress benchmarks. Here we present the steps to run the apps:

## Step 1: Setting up
* Setup the docker image for running the benchmarks
    `docker-compose build`
    `pip install -r scripts/00_requirements.txt`

* Install the applications locally (only required once)

    `docker-compose run benchpress bash install_benchmarks.sh`

## Step 2: Run monitoring daemon
This is required for reporting the metrics

    cd node-exporter
    docker-compose up

## Step 3: Run the benchmarks

* FIO
    ``` 
    docker-compose run benchpress python3 benchpress_cli.py -b benchmarks.yml -j jobs/jobs.yml run "fio aio" 
    ```
* Schbench
    ```
    docker-compose run benchpress python3 benchpress_cli.py -b benchmarks.yml -j jobs/jobs.yml run "schbench default"
    ```
    
* Gapbs 
    ```
    docker-compose run benchpress python3 benchpress_cli.py -b benchmarks.yml -j jobs/jobs.yml run "gapbs_bc"
    ```
* Nginx_Wrk
    ```
   docker-compose run benchpress python3 benchpress_cli.py -b benchmarks.yml -j jobs/jobs.yml run "nginx_wrk_bench default"
    ```
* Graph500
    ```
    docker-compose run benchpress python3 benchpress_cli.py -b benchmarks.yml -j jobs/jobs.yml run "graph500_omp_csr"
    ```
* Minebench 
    ```
    docker-compose run benchpress python3 benchpress_cli.py -b benchmarks.yml -j jobs/jobs.yml run "minebench_plsa default"
    ```

# Profiling Benchpress benchmarks
We are using a docker container based runtime for running the benchpress benchmarks. Here we present the steps to run the apps:


## Setting up
* Setup the docker image for running the benchmarks

    `docker-compose build`

* Install the applications locally (only required once)

    `docker-compose run benchpress bash install_benchmarks.sh`

## Run the benchmarks

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
* Silo
    ```
    docker-compose run benchpress python3 benchpress_cli.py -b benchmarks.yml -j jobs/jobs.yml run " silo default"
    ```
* Minebench 
    ```
    docker-compose run benchpress python3 benchpress_cli.py -b benchmarks.yml -j jobs/jobs.yml run "minebench_plsa default"
    ```

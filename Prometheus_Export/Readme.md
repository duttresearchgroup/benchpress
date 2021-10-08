## Selected Node Parameters 
- node_thermal_zone_temp(0.9200459453584183)
    - Zone temperature in Celsius
- node_schedstat_waiting_seconds_total( 0.7640739318235192)
    - Number of seconds spent by processing waiting for this CPU
- node_rapl_core_joules_total( 0.7161596648385933)
    - Current RAPL core value in joules
- node_rapl_dram_joules_total( 0.7156185871109084)
- node_vmstat_pgpgout( 0.7061262875825904)
    - proc/vmstat information field pgpgout
    - vmstat (virtual memory statistics) is a system utility that collects and displays information about system memory, 
processes, interrupts, paging and block I/O. Using vmstat, you can specify a sampling interval to observe system activity in near-real time
- node_pressure_cpu_waiting_seconds_total( 0.7007835069076795)
    - Total time in seconds that processes have waited for CPU time
- node_schedstat_timeslices_total( 0.6968588014916662)
    - Number of timeslices executed by CPU
- node_softnet_processed_total( 0.6963217659189634)
    - Number of processed packets
- process_virtual_memory_bytes( 0.6963048443835615)
    - Virtual memory size in bytes
- node_disk_reads_completed_total( 0.6160464583589014)
    - The total number of reads completed successfully
- node_memory_Percpu_bytes( 0.6003240968091709)
- node_disk_read_time_seconds_total_device_sda( 0.5721848986826082)
    - The total number of seconds spent by all reads
- node_cpu_scaling_frequency_hertz( 0.5372931087040026)
    - Current scaled CPU thread frequency in hertz
- node_disk_io_time_weighted_seconds_total( 0.5296272336922856)
    - The weighted # of seconds spent doing I/Os.
- node_disk_read_bytes_total_device_sda (0.49576758466306803)
    - The total number of bytes read successfully.
- node_disk_write_time_seconds_total(0.46838149327892536)
    - This is the total number of seconds spent by all writes.
- node_disk_io_time_seconds_total(0.46823752095377363)
    - Total seconds spent doing I/Os
- node_disk_writes_merged_total(0.46764013040355923)
    - The number of writes merged
- node_memory_Buffers_bytes(0.46726665111115967)
    - Memory information field Buffers_bytes
- node_memory_MemAvailable_bytes(0.46709098618015)
- node_disk_written_bytes_total(0.458658137486144)
    - The total number of bytes written successfully
- node_memory_MemFree_bytes(0.4543217484680648)
    - Memory information field MemFree_bytes
- node_forks_total(0.4509998075690015)
    - Total number of forks
- node_disk_reads_merged_total(0.4268421294182468)
    - The total number of reads merged
- node_disk_writes_merged_total(0.422866214268668)
    - The number of writes merged
- node_context_switches_total (0.40872751813869485)
    - Total number of context switches
- node_intr_total (0.39247035644104533)
    - Total number of interrupts serviced
- node_memory_Mlocked_bytes (0.35229376089396003)
    -  Memory information field Mlocked_bytes.
- node_memory_Unevictable_bytes (0.35229376089396003)
    - Memory information field Unevictable_bytes
## How to run the scripts

* fetch_data.py
    - generating data from prometheus
    ```
    python -l http://deep.ics.uci.edu:9090 -f data.csv --step 1
    ```

* print_corre.py
    - generate the most correlated parameters 
    ```
    python print_corre.py data.csv
    ```

#!/bin/bash

# Set CPU MHz  : 4460
# Turbo MHz(s) : 4600 4700 4800 4900
# Turbo Ratios : 121% 123% 126% 128%
# CPU 0 summary every 1 seconds...

# bash -c 'echo 1 > /sys/devices/system/cpu/cpu0/online'
bash -c 'echo 0 > /sys/devices/system/cpu/cpu1/online'
bash -c 'echo 0 > /sys/devices/system/cpu/cpu2/online'
bash -c 'echo 0 > /sys/devices/system/cpu/cpu3/online'
bash -c 'echo 0 > /sys/devices/system/cpu/cpu4/online'
bash -c 'echo 0 > /sys/devices/system/cpu/cpu5/online'
bash -c 'echo 1 > /sys/devices/system/cpu/cpu6/online'
bash -c 'echo 0 > /sys/devices/system/cpu/cpu7/online'
bash -c 'echo 0 > /sys/devices/system/cpu/cpu8/online'
bash -c 'echo 0 > /sys/devices/system/cpu/cpu9/online'
bash -c 'echo 0 > /sys/devices/system/cpu/cpu10/online'
bash -c 'echo 0 > /sys/devices/system/cpu/cpu11/online'

lscpu | grep On-line
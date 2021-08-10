#!/bin/bash
# Downloads and compiles schbench and fio, putting the binaries into ./benchmarks/

# benchmark binaries that we install here live in benchmarks/
BENCHMARKS_DIR="$(pwd)/benchmarks"
rm -rf $BENCHMARKS_DIR
mkdir -p $BENCHMARKS_DIR

./install_schbench.sh
./install_silo.sh
./install_fio.sh
./install_gapbs.sh
./install_nginx_wrk_benchmark.sh
./install_minebench.sh
./install_graph500.sh

echo "Benchmarks installed into ./benchmarks/"

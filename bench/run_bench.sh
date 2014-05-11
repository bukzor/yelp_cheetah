#!/usr/bin/env bash
set -e

HERE=$(dirname $(readlink -f $0))
cd $HERE/..

filename=bench/log/`date +%F_%T`.txt

make clean
virtualenv bench/venv --clear
. bench/venv/bin/activate
CHEETAH_C_EXT=false pip install .
./bench/runbench.py | tee -a "$filename"

make clean
virtualenv bench/venv --clear
. bench/venv/bin/activate
CHEETAH_C_EXT=true pip install .
./bench/runbench.py | tee -a "$filename"

#! /usr/bin/env bash

function run {
    pushd $1 
    echo "WD: " $PWD
    echo "CMD:" 
    nice -n 19 hwut "$2" > /dev/null &
    popd
    echo
}

hwut make clean

run TEST
run demo
run quex/code_base
run quex/engine
run quex/input
run quex/output


# Wait until all hwut jobs terminated
for job in `jobs -p`; do
    wait $job 
done

# Run 'hwut info' to collect the information
# hwut i

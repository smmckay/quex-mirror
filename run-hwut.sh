# hwut make clean

function run {
    pushd $1 
    echo "WD: " $PWD
    echo "CMD:" 
    nice -n 19 hwut "$2" > /dev/null &
    popd
    echo
}

run TEST
run demo/C
run demo/Cpp
run quex/TESTS
run quex/engine
run quex/input
run quex/output


# Wait until all hwut jobs terminated
for job in `jobs -p`; do
    wait $job 
done

# Run 'hwut info' to collect the information
# hwut i

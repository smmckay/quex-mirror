# hwut make clean

function run {
    pushd $1 
    echo "WD: " $PWD
    echo "CMD:" 
    nice -n 19 hwut "$2" &
    popd
    echo
}

run TEST
run demo/C
run demo/Cpp
run quex/TESTS

run quex/code_base/buffer/TESTS/navigation/TEST/ "test-Plain*" 
run quex/code_base/buffer/TESTS/navigation/TEST/ "test-Converter*" 

for dir in quex/code_base/buffer/TESTS/*; do
    if [[ "$dir" == *"navigation$"* ]]; then continue; fi
    run $dir
done
for dir in quex/code_base/buffer/TESTS/*; do
    if [[ "$dir" == *"navigation$"* ]]; then continue; fi
    run $dir
done
for dir in quex/code_base/*; do
    if [[ "$dir" == *"buffer$"* ]]; then continue; fi
    run $dir
done
for dir in quex/*; do
    if [[ "$dir" == *"code_base$"* ]]; then continue; fi
    run $dir
done

# Wait until all hwut jobs terminated
for job in `jobs -p`; do
    wait $job 
done

# Run 'hwut info' to collect the information
# hwut i

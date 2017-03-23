#! /usr/bin/env bash

function run {
    pushd $1 
    echo "WD: " $PWD
    echo "CMD:" 
    nice -n 19 hwut "$2" > /dev/null &
    popd
    echo
}

rm $(find -name cache.fly) -f
hwut make clean

run ./TEST
run ./quex/output/cpp/TEST
run ./quex/output/core/TEST
run ./quex/output/core/state/transition_map/TEST
run ./quex/output/graphviz/TEST
run ./quex/input/TEST
run ./quex/input/regular_expression/TEST
run ./quex/engine/misc/TEST
run ./quex/engine/TEST
run ./quex/engine/state_machine/algorithm/TEST
run ./quex/engine/state_machine/transformation/TEST
run ./quex/engine/state_machine/check/TEST
run ./quex/engine/state_machine/TEST
run ./quex/engine/state_machine/construction/TEST
run ./quex/engine/state_machine/algebra/TESTS/extra_operations/TEST
run ./quex/engine/state_machine/algebra/TESTS/subset/TEST
run ./quex/engine/state_machine/algebra/TESTS/fundamental_laws/TEST
run ./quex/engine/state_machine/algebra/TESTS/additional_laws/TEST
run ./quex/engine/state_machine/algebra/TESTS/basics/TEST
run ./quex/engine/loop/TEST
run ./quex/engine/analyzer/TEST
run ./quex/engine/analyzer/mega_state/path_walker/TEST
run ./quex/engine/analyzer/mega_state/template/TEST
run ./quex/engine/operations/TEST
run ./quex/TESTS/event-handling/TEST
run ./quex/TESTS/source-package/TEST
run ./quex/TESTS/match-precedence/TEST
run ./quex/TESTS/token-policies/TEST
run ./quex/TESTS/misc/TEST
run ./quex/TESTS/token-class/TEST
run ./quex/TESTS/include-stack/TEST
run ./quex/TESTS/loop/TEST
run ./quex/TESTS/code/TEST
run ./quex/TESTS/drop-outs/TEST
run ./quex/TESTS/did-you-mean/TEST
run ./quex/TESTS/command-line/TEST
run ./quex/TESTS/entry-exit/TEST
run ./quex/TESTS/errors-warnings/TEST
run ./quex/TESTS/indentation_count/TEST
run ./quex/TESTS/reset/TEST
run ./quex/code_base/converter_helper/TEST
run ./quex/code_base/TEST
run ./quex/code_base/buffer/lexatoms/converter/iconv/TEST
run ./quex/code_base/buffer/lexatoms/converter/icu/TEST
run ./quex/code_base/buffer/bytes/TEST
run ./quex/code_base/buffer/TESTS/navigation/TEST
run ./quex/code_base/buffer/TESTS/misc/TEST
run ./quex/code_base/buffer/TESTS/move/TEST
run ./quex/code_base/buffer/TESTS/load/TEST
run ./quex/code_base/analyzer/TEST
run ./quex/code_base/analyzer/struct/TEST
run ./demo/C/TEST
run ./demo/TEST
run ./demo/Cpp/TEST


# Wait until all hwut jobs terminated
for job in `jobs -p`; do
    wait $job 
done

# Run 'hwut info' to collect the information
# hwut i

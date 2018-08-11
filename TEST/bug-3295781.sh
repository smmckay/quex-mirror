#! /usr/bin/env bash
bug=3295781
if [[ $1 == "--hwut-info" ]]; then
    echo "remcobloemen1: $bug Duplicate label with Template and Path Compression"
    echo "HAPPY: [0-9]+;"
    exit
fi

tmp=`pwd`
cd $bug/ 
quex --cbm -i test.qx -o Simple --path-compression-uniform --template-compression --language C  --debug-exception >&1

cd Simple
awk '( /Simple_[XY]_analyzer_function/ && ! /=/) || /__quex_debug_path_walker_state/ || /__quex_debug_template_state/' Simple.c | sed -e 's/^ *//'

cd ..

echo "## Compile: No output is good output"
gcc -I. -c Simple/Simple.c -Wall -Werror 2>&1

# cleansening
rm -rf Simple*
cd $tmp


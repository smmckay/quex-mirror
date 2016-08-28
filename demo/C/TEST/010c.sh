#! /usr/bin/env bash
if [[ $1 == "--hwut-info" ]]; then
    echo "demo/010: Pointing to Buffer Memory;"
    exit
fi
cd $QUEX_PATH/demo/C/010

if [[ "$2" == "FIRST" ]]; then
    make clean >& /dev/null
fi

$QUEX_PATH/TEST/call-make.sh point.exe
$QUEX_PATH/TEST/valgrindi.sh tmp.txt ./point.exe 
cat tmp.txt; rm -f tmp.txt

if [[ "$3" == "LAST" ]]; then
    make clean >& /dev/null
fi


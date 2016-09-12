#! /usr/bin/env bash
if [[ $1 == "--hwut-info" ]]; then
    echo "demo/010: Manual Buffer Filling (w/o Converter)"
    echo "CHOICES:  feeder-plain, feeder-converter, gavager-plain, gavager-converter, point-plain;"
    exit
fi
cd $QUEX_PATH/demo/C/010

if [[ "$2" == "FIRST" ]]; then
    make clean >& /dev/null
fi
if [ -z "$2" ]; then
    make clean
fi

$QUEX_PATH/TEST/call-make.sh $1.exe
$QUEX_PATH/TEST/valgrindi.sh tmp.txt ./$1.exe 
cat tmp.txt; rm -f tmp.txt

if [[ "$3" == "LAST" ]]; then
    make clean >& /dev/null
fi


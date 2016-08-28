#! /usr/bin/env bash
if [[ $1 == "--hwut-info" ]]; then
    echo "demo/010: Manual Buffer Filling (w/o Converter)"
    echo "CHOICES:  syntactic-fill, syntactic-copy, arbitrary-fill, arbitrary-copy;"
    exit
fi
cd $QUEX_PATH/demo/C/010

if [[ "$2" == "FIRST" ]]; then
    make clean >& /dev/null
fi

$QUEX_PATH/TEST/call-make.sh lexer.exe 
$QUEX_PATH/TEST/valgrindi.sh tmp.txt ./lexer.exe $(echo $1 | tr "-" " ")
cat tmp.txt; rm -f tmp.txt

if [[ "$3" == "LAST" ]]; then
    make clean >& /dev/null
fi


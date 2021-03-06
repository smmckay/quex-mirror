#! /usr/bin/env bash
bug=3039173
if [[ $1 == "--hwut-info" ]]; then
    echo "fschaef: $bug On Mismatch: abort()"
    echo "HAPPY: Simple.c:[0-9]+:;"
    exit
fi

tmp=`pwd`
cd $bug/ 

quex --cbm -i simple.qx -o Simple --language C
gcc ../lexer.c Simple/Simple.c -I. -I$QUEX_PATH -o lexer -Wall -Werror
./lexer example.txt 2> tmp.txt
cat tmp.txt
rm -f tmp.txt
rm -rf Simple* 
rm -f lexer

# cleansening
cd $tmp

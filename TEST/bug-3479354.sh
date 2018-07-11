#! /usr/bin/env bash
bug=3479354
if [[ $1 == "--hwut-info" ]]; then
    echo "clemwang: $bug Reversed (right to left) Pattern Definition;"
    echo "HAPPY: [0-9]+;"
    exit
fi

tmp=`pwd`
cd $bug/ 
quex --cbm -i test.qx -o EasyLexer --language C --comment-state-machine --debug-exception
cd EasyLexer
awk 'BEGIN {w=0} /BEGIN:/ {w=1;} // {if(w) print;} /END:/ {w=0;}' EasyLexer.c
cd ..

# cleansening
rm -rf EasyLexer*
cd $tmp

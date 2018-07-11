#! /usr/bin/env bash
bug=1948456
if [[ $1 == "--hwut-info" ]]; then
    echo "fschaef: $bug (feature) Inheritance Info"
    echo "HAPPY: [ 0-9]+;"
    exit
fi

tmp=`pwd`
cd $bug/ 
quex --cbm -i simple.qx -o Simple --comment-mode-patterns --debug-exception
awk 'BEGIN { allow_f = 0; } /MODE: FOUR/ { allow_f = 1; } /^[ \t]*\*/ { if( allow_f) print; } /END: MODE PATTERNS/ { exit; }' Simple/Simple.cpp

# cleansening
rm -rf Simple Simple.cpp Simple-* *.o tmp.txt
cd $tmp

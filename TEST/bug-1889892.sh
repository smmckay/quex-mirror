#! /usr/bin/env bash
bug=1889892
if [[ $1 == "--hwut-info" ]]; then
    echo "sphericalcow: $bug x, X or followed by a non-hex digit crashes 0.19.4"
    echo "HAPPY: qx:[0-9]+:;"
    exit
fi

tmp=`pwd`
cd $bug/ 
echo "(1)"
quex --cbm -i error.qx 
echo "(2)"
quex --cbm -i error-1.qx 
echo "(3)"
quex --cbm -i error-2.qx 
echo "(4)"
quex --cbm -i error-3.qx 
echo "(5)"
quex --cbm -i error-4.qx 
echo "(6)"
quex --cbm -i error-5.qx 

rm -rf Lexer
cd $tmp

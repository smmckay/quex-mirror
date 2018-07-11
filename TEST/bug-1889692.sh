#! /usr/bin/env bash
bug=1889692
if [[ $1 == "--hwut-info" ]]; then
    echo "sphericalcow: $bug 0.19.4 does not gracefully handle unbalanced quotations"
    exit
fi

tmp=`pwd`
cd $bug/ 
echo "Use Case (1)"
quex --cbm -i error.qx 
echo 

echo "Use Case (2)"
quex --cbm -i error-2.qx 
echo 

rm -rf Lexer
cd $tmp

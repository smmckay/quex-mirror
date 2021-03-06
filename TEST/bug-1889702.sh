#! /usr/bin/env bash
bug=1889702
if [[ $1 == "--hwut-info" ]]; then
    echo "sphericalcow: $bug 0.19.4 forbids derived modes that only add event handlers"
    echo "HAPPY: ^error-3.qx:[0-9]+:;"
    exit
fi

tmp=`pwd`
cd $bug/ 
echo "(1)"
quex --cbm -i error.qx -o Simple
echo

echo "(2)"
quex --cbm -i error-2.qx -o Simple
echo

echo "(3)"
quex --cbm -i error-3.qx -o Simple
echo

# cleansening
rm -rf Simple Simple.cpp Simple-token_ids Simplism
cd $tmp

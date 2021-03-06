#! /usr/bin/env bash
bug=2819023
if [[ $1 == "--hwut-info" ]]; then
    echo "wryun: $bug 0.41.2 Valid pattern definition fails"
    exit
fi

tmp=`pwd`
cd $bug/ 
quex --cbm -i nonsense.qx -o Simple

# cleansening
rm -rf Simple Simple.cpp Simple-token_ids Simplism
cd $tmp

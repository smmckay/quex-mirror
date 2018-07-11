#! /usr/bin/env bash
bug=1952747
if [[ $1 == "--hwut-info" ]]; then
    echo "fschaef: $bug TKN_TERMINATION"
    exit
fi

tmp=`pwd`
cd $bug/ 
quex --cbm -i simple.qx -o Simple --debug-exception
cd Simple
grep -e user_specified_tkn_termination_handler Simple.cpp
cd ..
# cleansening
rm -rf Simple Simple.cpp Simple-*
cd $tmp

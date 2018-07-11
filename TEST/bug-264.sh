#! /usr/bin/env bash
bug=264
if [[ $1 == "--hwut-info" ]]; then
    echo "jdavidberger: $bug 0.64.6 Incorrect column numbering with post conditions"
    exit
fi

tmp=`pwd`
cd $bug/ 
quex --cbm -i test.qx -o Simple --debug-exception
cd Simple
cat Simple.cpp | awk 'BEGIN { f=0; } /23456789/ { f=1; } /{/ { f=0; } /counter/ { if( f == 1 ) { print; }}'
cd ..

rm -rf Simple*
cd $tmp

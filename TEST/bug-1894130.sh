#! /usr/bin/env bash
bug=1894130
if [[ $1 == "--hwut-info" ]]; then
    echo "sphericalcow: $bug 0.20.6 can list wrong mode as circuluar inheritance"
    exit
fi

tmp=`pwd`
cd $bug/ 
quex --cbm -i error.qx -o Simple  # --debug-exception

# cleansening
rm -rf Simple  Simple.cpp Simple-token_ids Simplism
cd $tmp

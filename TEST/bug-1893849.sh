#! /usr/bin/env bash
bug=1893849
if [[ $1 == "--hwut-info" ]]; then
    echo "sphericalcow: $bug 0.20.5 allows engine names that are not valid identifiers"
    exit
fi

tmp=`pwd`
cd $bug/ 
quex --cbm -i error.qx -o Engin-e
rm -rf Engin-e*
cd $tmp

#! /usr/bin/env bash
bug=2262537
if [[ $1 == "--hwut-info" ]]; then
    echo "marcoantonelli: $bug (feature) Allow Nothing is fine in define section"
    exit
fi

tmp=`pwd`
cd $bug/ 
echo "Error Case:\n"
quex --cbm -i error.qx -o Simple

echo "Good Case:\n"
quex --cbm -i test.qx -o Simple

# cleansening
rm -rf Simple Simple.cpp Simple-* *.o tmp.txt
cd $tmp

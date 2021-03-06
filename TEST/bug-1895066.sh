#! /usr/bin/env bash
bug=1895066
if [[ $1 == "--hwut-info" ]]; then
    echo "sphericalcow: $bug 0.20.8 #line directive after header contents missing"
    echo "HAPPY: line [0-9]+;"
    exit
fi

tmp=`pwd`
cd $bug/ 
quex --cbm -i error.qx -o Simple

echo
echo 'Output from constructed header:_______________________________________'
echo
cd Simple
../../quex_pathify.sh Simple | awk '/\# *line/' 
cd ..

# cleansening
rm -rf Simple
cd $tmp

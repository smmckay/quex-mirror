#! /usr/bin/env bash
bug=1894185
if [[ $1 == "--hwut-info" ]]; then
    echo "sphericalcow: $bug Unbalanced quote and double quote in header/init/body blocks in 0.20.6"
    exit
fi

tmp=`pwd`
cd $bug/ 
echo '(1)'
quex --cbm -i error.qx -o Simple
echo

echo '(2)'
quex --cbm -i error-2.qx -o Simple

# cleansening
rm -rf Simple
cd $tmp

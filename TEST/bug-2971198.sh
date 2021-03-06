#! /usr/bin/env bash
bug=2971198
if [[ $1 == "--hwut-info" ]]; then
    echo "kromaks: $bug 0.48.1 Parsing long REs"
    exit
fi

tmp=`pwd`
cd $bug/ 
quex --cbm -i error.qx -o Simple --debug-exception >& tmp.txt

cat tmp.txt | awk '(/[Ww][Aa][Rr][Nn][Ii][Nn][Gg]/ || /[Ee][Rr][Rr][Oo][Rr]/) && ! /ASSERTS/ '
rm tmp.txt

echo "||||"
ls Simple/Simple* | cut -d ' ' -f 1 | sort 
echo "||||"

# cleansening
rm -rf Simple*

cd $tmp

#! /usr/bin/env bash
bug=1935701
if [[ $1 == "--hwut-info" ]]; then
    echo "sphericalcow: $bug 0.24.7 buffer handling size mismatch"
    echo "CHOICES: FILE, fstream;"
    exit
fi

tmp=`pwd`
cd $bug/ 

if [ "$2" == "FIRST" ] || [ -z "$2"  ]; then 
    make clean >& /dev/null
fi

make >& tmp.txt
cat tmp.txt | awk '(/[Ww][Aa][Rr][Nn][Ii][Nn][Gg]/ || /[Ee][Rr][Rr][Oo][Rr]/) && ! /ASSERTS/ '
rm tmp.txt

./bug-1935701.exe $1

# cleansening
if [ "$3" == "LAST" ] || [ -z "$3" ]; then 
    make clean >& /dev/null
fi
cd $tmp

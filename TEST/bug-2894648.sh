#! /usr/bin/env bash
bug=2894648
if [[ $1 == "--hwut-info" ]]; then
    echo "nobody: $bug 0.46.2 Backslashed . is unknown to quex"
    echo "HAPPY: [ 0-9]+;"
    exit
fi

tmp=`pwd`
cd $bug/ 
quex --cbm -i test.qx -o Simple --comment-state-machine --language C >& tmp.txt
cat tmp.txt | awk '(/[Ww][Aa][Rr][Nn][Ii][Nn][Gg]/ || /[Ee][Rr][Rr][Oo][Rr]/) && ! /ASSERTS/ '
awk 'BEGIN {w=0} /BEGIN:/ {w=1;} // {if(w) print;} /END:/ {w=0;}' Simple/Simple.c

# python show.py
rm tmp.txt

# cleansening
rm -rf Simple*
cd $tmp

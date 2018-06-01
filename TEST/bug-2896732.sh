#! /usr/bin/env bash
bug=2896732
if [[ $1 == "--hwut-info" ]]; then
    echo "nazim-can-bedir: $bug 0.46.2 - Memory leak"
    exit
fi
echo "Note: the important phrase is 'no leaks are possible'."
tmp=`pwd`
cd $bug/ 
make >& tmp.txt
cat tmp.txt | awk '(/[Ww][Aa][Rr][Nn][Ii][Nn][Gg]/ || /[Ee][Rr][Rr][Oo][Rr]/) && ! /ASSERTS/ '
$QUEX_PATH/TEST/valgrindi.sh valgrint-out.txt ./uXa example.txt >& /dev/null
cat valgrint-out.txt
rm -f valgrint-out.txt

# cleansening
make clean >& /dev/null
cd $tmp

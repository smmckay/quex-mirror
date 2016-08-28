#! /usr/bin/env bash
if [[ $1 == "--hwut-info" ]]; then
    echo "demo/010: Pointing to Buffer Memory;"
    exit
fi
cd $QUEX_PATH/demo/Cpp/010

if [[ "$2" == "FIRST" ]]; then
    make clean >& /dev/null
fi

make point.exe ASSERTS_ENABLED_F=YES >& tmp.txt

cat tmp.txt | awk ' ! /gcc/' | awk '/[Ww][Aa][Rr][Nn][Ii][Nn][Gg]/ || /[Ee][Rr][Rr][Oo][Rr]/ { print; }' | awk ' !/out of range/ && ! /getline/'
rm tmp.txt

$QUEX_PATH/TEST/valgrindi.sh tmp.txt ./point.exe >& tmp.txt

cat tmp.txt; rm -f tmp.txt

if [[ "$3" == "LAST" ]]; then
    make clean >& /dev/null
fi


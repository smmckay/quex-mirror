#! /usr/bin/env bash
if [[ $1 == "--hwut-info" ]]; then
    echo "demo/011b: Engine Encoding UTF16"
    echo "CHOICES:  LE, BE;"
    echo "SAME;"
    exit
fi
cd $QUEX_PATH/demo/C/011
make clean >& /dev/null
make utf16-lexer-other >& tmp.txt
cat tmp.txt | awk '(/[Ww][Aa][Rr][Nn][Ii][Nn][Gg]/ || /[Ee][Rr][Rr][Oo][Rr]/) && ! /ASSERTS/ && ! /-Werror/'
rm tmp.txt
$QUEX_PATH/TEST/valgrindi.sh tmp.txt ./utf16-lexer-other $1 
cat tmp.txt; rm -f tmp.txt

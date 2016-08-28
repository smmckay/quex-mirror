#! /usr/bin/env bash
if [[ $1 == "--hwut-info" ]]; then
    echo "demo/011: Engine Encoding (Example ISO8859-7)"
    echo "CHOICES:  iso8859-7, utf8, utf16-be, utf16-le;"
    echo "SAME;"
    exit
fi

choice=$1
special=''

case $choice in 
   "utf16-le") choice="utf16"; special="LE";;
   "utf16-be") choice="utf16"; special="BE";;
esac


cd $QUEX_PATH/demo/C/011
make clean >& /dev/null
make $choice-lexer 2> tmp.txt 1> /dev/null
cat tmp.txt | awk ' !/gcc/ && !/codec/ && !/-Werror/ && !/[Ww][Aa][Rr][Nn][Ii][Nn][Gg]/ && !/[Ee][Rr][Rr][Oo][Rr]/ { print; }'
rm tmp.txt
$QUEX_PATH/TEST/valgrindi.sh./$choice-lexer $special >& tmp.txt
cat tmp.txt; rm -f tmp.txt

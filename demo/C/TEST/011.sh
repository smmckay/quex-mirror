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
$QUEX_PATH/TEST/call-make.sh clean $choice-lexer
$QUEX_PATH/TEST/valgrindi.sh tmp.txt ./$choice-lexer $special 
cat tmp.txt; rm -f tmp.txt

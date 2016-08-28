#! /usr/bin/env bash
if [[ $1 == "--hwut-info" ]]; then
    echo "demo/010: Manual Buffer Filling (w/ Converter)"
    echo "CHOICES:  syntactic-fill, syntactic-copy, arbitrary-fill, arbitrary-copy;"
    exit
fi
cd $QUEX_PATH/demo/Cpp/010

if [[ "$2" == "FIRST" ]]; then
make clean >& /dev/null
fi

make  lexer_utf8.exe ASSERTS_ENABLED_F=YES >& tmp.txt

cat tmp.txt | awk ' ! /gcc/' | awk '/[Ww][Aa][Rr][Nn][Ii][Nn][Gg]/ || /[Ee][Rr][Rr][Oo][Rr]/ { print; }' | awk ' !/out of range/ && ! /getline/'
rm tmp.txt

case $1 in
    syntactic-fill) $QUEX_PATH/TEST/valgrindi.sh tmp.txt ./lexer_utf8.exe syntactic fill 
    ;;
    syntactic-copy) $QUEX_PATH/TEST/valgrindi.sh tmp.txt ./lexer_utf8.exe syntactic copy
    ;;
    arbitrary-fill) $QUEX_PATH/TEST/valgrindi.sh tmp.txt ./lexer_utf8.exe arbitrary fill
    ;;
    arbitrary-copy) $QUEX_PATH/TEST/valgrindi.sh tmp.txt ./lexer_utf8.exe arbitrary copy
    ;;
esac

cat tmp.txt
rm -f tmp.txt

if [[ $3 == "LAST" ]]; then
    make clean >& /dev/null
fi


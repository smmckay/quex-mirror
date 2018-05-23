#! /usr/bin/env bash
if [[ $1 == "--hwut-info" ]]; then
    echo "Source Packager: C++;"
    echo "CHOICES: plain, codec, codec-utf8, codec-utf16, no-counter, manual-token-class, customized-token-class;"
    echo "SAME;"
    exit
fi

if [ -d pkg ]; then
    rm -rf pkg/*
else
    mkdir pkg
fi

case $1 in
    plain) 
        option='-i simple.qx '
        ;;
    codec)
        option='-i simple.qx --encoding iso8859_7'
        ;;
    codec-utf8)
        option='-i simple.qx --encoding utf8'
        ;;
    codec-utf16)
        option='-i simple.qx --encoding utf16 --bes 2'
        ;;
    no-counter)
        option='-i simple.qx --no-count-lines --no-count-columns'
        ;;
    customized-token-class)
        option='-i example_token-cpp.qx simple.qx'
        ;;
    manual-token-class)
        cp example_token-cpp.h pkg/
        option='-i simple.qx --token-class-file example_token-cpp.h --token-class Test::MyToken'
        ;;
esac

echo "(0) Running Quex (no output is good output)"
quex $option -o EasyLexer --odir pkg 

echo "(1) Running g++ (no output is good output)"
g++  -I. pkg/EasyLexer.cpp -o pkg/EasyLexer.o -c -Wall -Werror -W

echo "(2) Double check that output file exists"
ls    pkg/EasyLexer.o 2> tmp.txt
cat tmp.txt

echo "(2.1) Double check that nothing in current directory. (no output is good output)."
ls    EasyLexer* 2> tmp.txt
cat tmp.txt

rm -rf tmp.txt pkg/EasyLexer



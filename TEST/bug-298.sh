#! /usr/bin/env bash
bug=298
if [[ $1 == "--hwut-info" ]]; then
    echo "patrikj-kt: $bug Quex exception in loop generation."
    exit
fi

tmp=`pwd`
cd $bug/ 
echo
echo "No output is good output (make)"
make 
echo "(done)"
echo "List of generated files:"
ls ecmascript_lexer-* | sort 
ls ecmascript_lexer.cpp
ls ecmascript_lexer
echo "<terminated>"

make clean >& /dev/null
cd $tmp

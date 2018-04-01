#! /usr/bin/env bash
bug=300
if [[ $1 == "--hwut-info" ]]; then
    echo "patrikj-kt: $bug Missing error message on non-existing mode."
    exit
fi

tmp=`pwd`
cd $bug/ 
quex -i ecmascript.qx --token-id-prefix TOK_DECLIT 2>&1 

rm -rf Lexer
cd $tmp

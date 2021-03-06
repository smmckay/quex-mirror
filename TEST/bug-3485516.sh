#! /usr/bin/env bash
bug=3485516
if [[ $1 == "--hwut-info" ]]; then
    echo "clemwang: $bug 0.60.1 0.60.1 Exception Handling Disorder"
    exit
fi

tmp=`pwd`
cd $bug/ 
quex --cbm -i uuu.qx -o UuuLexer --token-id-prefix UUU_TKN_ 2>&1
rm -rf UuuLexer
cd $tmp

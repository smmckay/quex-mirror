#! /usr/bin/env bash
bug=1889086
if [[ $1 == "--hwut-info" ]]; then
    echo "sphericalcow: $bug Single state mode causes quex to crash"
    exit
fi

tmp=`pwd`
cd $bug 
../quex_pathify.sh --string `pwd`
echo "tokens in .qx files _____________________________________"
echo '(1)'
quex --cbm -i error-1.qx -o Simple
echo '(2)'
quex --cbm -i error-2.qx -o Simple
echo '(3)'
quex --cbm -i error-3.qx -o Simple
echo 
echo "tokens on command line __________________________________"
echo '(1)'
quex --cbm --token-id-prefix TKN-
echo '(2)'
quex --cbm --token-id-prefix SMOEREBROED
rm -rf Lexer Simple  Simple.cpp  Simple-token_ids
cd $tmp

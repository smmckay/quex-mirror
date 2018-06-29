#! /usr/bin/env bash
bug=3009642
if [[ $1 == "--hwut-info" ]]; then
    echo "rofr3: $bug 0.48.3 Begin of Line Precondition flag"
    exit
fi

tmp=`pwd`
cd $bug/ 

echo "Check whether the begin of line support flag is set propperly."
echo 
echo "(1) A grammar with a begin of line pre-condition."
quex -i with-begin-of-line.qx -o Simple --debug-exception
cd Simple
grep _lexatom_before_lexeme_start Simple.cpp | sort -u
cd ..

echo "(2) A grammar without a begin of line pre-condition."
quex -i without-begin-of-line.qx -o Simple --debug-exception
cd Simple
grep _lexatom_before_lexeme_start Simple.cpp
cd ..

rm -rf Simple*
cd $tmp

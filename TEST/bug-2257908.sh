#! /usr/bin/env bash
bug=2257908
if [[ $1 == "--hwut-info" ]]; then
    echo "marcoantonelli: $bug Quex does not terminate lexer generation"
    exit
fi

tmp=`pwd`

cd $bug/ 
file=`pwd`/error.qx
bash ../test_that_it_does_not_take_too_long.sh $file 20

# cleansening
rm -rf Lexer Lexer-* Lexer.cpp 

cd $tmp

#! /usr/bin/env bash
bug=2819022
if [[ $1 == "--hwut-info" ]]; then
    echo "wryun: $bug 0.41.2 Pre-condition match causes issues;"
    echo "CHOICES: 0, 1, 2, 3;"
    exit
fi

tmp=`pwd`
cd $bug/ 
make CASE=$1 >& /dev/null
echo ----------------------------------
cat error-$1.txt
echo ----------------------------------
./lexer error-$1.txt

make clean >& /dev/null
cd $tmp

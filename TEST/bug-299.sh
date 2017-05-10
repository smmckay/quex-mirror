#! /usr/bin/env bash
bug=299
if [[ $1 == "--hwut-info" ]]; then
    echo "patrikj-kt: $bug LoopRestartP -- generated code does not compile"
    exit
fi

tmp=`pwd`
cd $bug/ 
make lexer >& tmp.txt
cat tmp.txt | awk '(/[Ww][Aa][Rr][Nn][Ii][Nn][Gg]/ || /[Ee][Rr][Rr][Oo][Rr]/) && ! /ASSERTS/ '
rm tmp.txt
bash ../valgrindi.sh tmp.txt ./lexer 
cat tmp.txt
rm tmp.txt

# cleansening
make clean >& /dev/null
cd $tmp

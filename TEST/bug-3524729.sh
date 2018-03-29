#! /usr/bin/env bash
bug=3524729
if [[ $1 == "--hwut-info" ]]; then
    echo "sbellon: $bug 0.62.4 token_type distinct members cause overloading error"
    exit
fi

tmp=`pwd`
cd $bug/ 
make lexer | bash ../quex_pathify.sh
rm -rf Lexer* tmp.txt
cd $tmp
echo "<terminated>"

#! /usr/bin/env bash
bug=3082041
if [[ $1 == "--hwut-info" ]]; then
    echo "fschaef: $bug 0.52.4 Buffer Memory Size not Accepted"
    exit
fi

tmp=`pwd`
cd $bug/ 
quex -i simple.qx -o EasyLexer
g++ -I. test.cpp EasyLexer/EasyLexer.cpp -o test \
    -DQUEX_SETTING_BUFFER_FALLBACK_N_EXT=0 \
    -DQUEX_OPTION_ASSERTS_WARNING_MESSAGE_DISABLED_EXT \
    -DQUEX_SETTING_BUFFER_SIZE_EXT=512 \
    -Wall -Werror >& tmp.txt

valgrind --log-file=tmp-valgrind.log --leak-check=full --show-leak-kinds=all \
         ./test > tmp.txt 2>&1
python ../show-valgrind.py tmp.txt


# cleaning
#rm tmp.txt
rm -rf EasyLexer*
rm -f test
rm -f tmp*
cd $tmp

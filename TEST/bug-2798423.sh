#! /usr/bin/env bash
bug=2798423
if [[ $1 == "--hwut-info" ]]; then
    echo "sphericalcow: $bug 0.39.4 token_type default __copy function does not compile"
    exit
fi

tmp=`pwd`
cd $bug/ 
quex -i simple.qx -o Simple --suppress 15 >& tmp.txt
cat tmp.txt
rm -f tmp.txt

echo "No error -- is just fine"
gcc -c -Wall -Werror -I$QUEX_PATH -I. Simple/*.cpp >& tmp.txt
cat tmp.txt
rm -f tmp.txt
ls -f *.o

# cleansening
rm -rf Simple*
cd $tmp

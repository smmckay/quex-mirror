#! /usr/bin/env bash
bug=3077292
if [[ $1 == "--hwut-info" ]]; then
    echo "ymarkovitch: $bug 0.52.3 Compilation Error With DEBUG_MODE_TRANSITIONS"
    exit
fi

tmp=`pwd`
cd $bug/ 
rm -rf Simple.o >& /dev/null

bash ../call-make.sh all 

echo "Confirm lexer has been created"
ls Simple.o >& tmp.txt
cat tmp.txt

# cleansening
make clean >& /dev/null

cd $tmp

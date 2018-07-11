#! /usr/bin/env bash
bug=3403249
if [[ $1 == "--hwut-info" ]]; then
    echo "ollydbg: $bug 0.61.2 Non UTF8 encoding for *.qx files not detected."
    echo "CHOICES: GBK, utf16, utf16-with-bom, utf8-error, utf8, utf8-with-bom;"
    exit
fi

tmp=`pwd`
cd $bug/ 
quex --cbm -i $1.qx -b 2 -o Simple >& tmp.txt
cat tmp.txt 
cd Simple
if [ -e Simple ]; then
    echo "||||"
    ls Simple* 
    echo "||||"
fi
cd ..
rm tmp.txt
rm -rf Simple*

cd $tmp

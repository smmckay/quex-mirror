#! /usr/bin/env bash
bug=2146712
if [[ $1 == "--hwut-info" ]]; then
    echo "yaroslav_xp: $bug (feature) output directory parameter for the command line;"
    echo "CHOICES: Normal, NotExist, NoWrite;"
    exit
fi

tmp=`pwd`
cd $bug/ 

chmod u+w x/y/z >& /dev/null
rm -rf a/b/c/d
rm -rf a/b/c/x
rm -rf x/y/z
chmod u-w x/y/z >& /dev/null

case $1 in
    "Normal")   odir=a/b/c/d;;
    "NotExist") odir=a/b/c/x;;
    "NoWrite")  odir=x/y/z;;
esac

quex -i simple.qx --output-directory $odir
find -path "*.svn*" -prune -or -print | grep $odir | grep -v lib | sort

# cleansening
rm -rf Lexer
cd $tmp

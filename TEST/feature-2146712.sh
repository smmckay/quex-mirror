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
rm -rf a/b/c/writeable/*     # 
rm -rf a/b/c/not-existent
rm -rf x/y/z/*
chmod u-w x/y/z >& /dev/null

case $1 in
    "Normal")   odir=a/b/c/writeable;     mkdir -p $odir; chmod u+w $odir;;
    "NotExist") odir=e/f/g/not-existent;  mkdir -p $odir; rm -rf $odir;;
    "NoWrite")  odir=h/i/j/not-writeable; mkdir -p $odir; chmod u-w $odir;;
esac

quex -i simple.qx --output-directory $odir
find -path "*.svn*" -prune -or -print | grep $odir | grep -v lib | sort

# cleansening
rm -rf a # 
rm -rf x
cd $tmp

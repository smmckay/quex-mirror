#! /usr/bin/env bash
bug=2146712
if [[ $1 == "--hwut-info" ]]; then
    echo "yaroslav_xp: $bug (feature) output directory parameter for the command line;"
    echo "CHOICES: Normal, NotExist, NoWrite;"
    exit
fi

tmp=`pwd`
cd $bug/ 

rm a/b/c/d/* -f
chomd u+w x/y/z
rm x/y/z/* -f
chmod u-w x/y/z

if [[ $1 == "Normal" ]]; then
    quex -i simple.qx --output-directory a/b/c/d
    echo "||||"
    find -path "*.svn*" -prune -or -print 
    echo "||||"
    rm a/b/c/d/Lexer*
fi
if [[ $1 == "NotExist" ]]; then
    quex -i simple.qx --output-directory a/b/c/x
    echo "||||"
    find -path "*.svn*" -prune -or -print
    echo "||||"
fi
if [[ $1 == "NoWrite" ]]; then
    quex -i simple.qx --output-directory x/y/z
    echo "||||"
    find -path "*.svn*" -prune -or -print 
    echo "||||"
fi

# cleansening
rm -f Lexer.cpp Lexer-token_ids 
cd $tmp

#! /usr/bin/env bash
bug=293
if [[ $1 == "--hwut-info" ]]; then
    echo "Dizzzy:  $bug 0.66.5: Encoding running on wchar_t;"
    echo "CHOICES: good, bad, invokation;"
    echo "HAPPY: [0-9]+;"
    exit
fi

tmp=`pwd`
cd 293

case $1 in
    good)
        make lexer 2>&1 | awk '(/[Ww][Aa][Rr][Nn][Ii][Nn][Gg]/ || /[Ee][Rr][Rr][Oo][Rr]/) && ! /ASSERTS/ '
        ./lexer good
        ;;
    bad)
        make lexer 2>&1 | awk '(/[Ww][Aa][Rr][Nn][Ii][Nn][Gg]/ || /[Ee][Rr][Rr][Oo][Rr]/) && ! /ASSERTS/ '
        ./lexer bad
        ;;
    invokation)
        make Message0;
        make Message1;
        make Message2;
        make Message3;
        ;;
esac

if [[ "$3" = "LAST" ]] || [[ "$3" = "" ]]; then 
    make clean
fi

cd $tmp

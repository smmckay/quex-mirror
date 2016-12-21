#! /usr/bin/env bash
bug=293
if [[ $1 == "--hwut-info" ]]; then
    echo "Dizzzy:   $bug 0.66.5: Encoding running on wchar_t"
    echo "CHOICES: good, bad, error-message;"
    exit
fi

tmp=`pwd`
cd 293

case $1 in
    good)
        make lexer 2 >& 1 | awk '(/[Ww][Aa][Rr][Nn][Ii][Nn][Gg]/ || /[Ee][Rr][Rr][Oo][Rr]/) && ! /ASSERTS/ '
        ./lexer
        ;;
    bad)
        make lexer >& tmp.txt
        cat tmp.txt | awk '(/[Ww][Aa][Rr][Nn][Ii][Nn][Gg]/ || /[Ee][Rr][Rr][Oo][Rr]/) && ! /ASSERTS/ '
        rm tmp.txt
        ./lexer
        ;;
    error-message)
        make ErrorMessage
        ;;
esac


# cleansening
make clean >& /dev/null
cd $tmp

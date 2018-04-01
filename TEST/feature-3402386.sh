#! /usr/bin/env bash
bug=3402386
if [[ $1 == "--hwut-info" ]]; then
    echo "ollydbg: $bug Option --language dot;"
    echo "CHOICES: hex, utf8;"
    echo "HAPPY:   state_machine_[0-9]+;"
    exit
fi

tmp=`pwd`
cd $bug/ 

case $1 in
    utf8)
    quex -i test.qx --language dot --debug-exception --normalize
    cat ME_*.dot
    cat ME.dot
    cat ME-pre*.dot
    ;;

    hex)
    quex -i test.qx --language dot --character-display hex --debug-exception --normalize
    cat ME_*.dot
    cat ME.dot
    cat ME-pre*.dot
    ;;
esac

# cleansening
rm -rf Lexer *.dot

cd $tmp

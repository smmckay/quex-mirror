#! /usr/bin/env bash
bug=257
if [[ $1 == "--hwut-info" ]]; then
    echo "enmarabrams: $bug Hang-up on recursive --foreign-token-id-file"
    echo "HAPPY: ^include_me.h:[0-9]+:;"
    exit
fi

tmp=`pwd`
cd $bug/ 

quex -i nonsense.qx --foreign-token-id-file include_me.h 2>&1 -o EasyLexer --foreign-token-id-file-show --debug-exception

echo
echo Generated Files:
cd EasyLexer
echo "||||"
ls EasyLexer* | cut -f 1
echo "||||"
cd ..
rm -rf EasyLexer*

# cleansening
cd $tmp

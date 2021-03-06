#! /usr/bin/env bash
bug=3235790
if [[ $1 == "--hwut-info" ]]; then
    echo "jmarsik: 0.58.2 history effect in UCS database interface: $bug "
    exit
fi

tmp=`pwd`
cd $bug/ 

quex --cbm -i simple.qx -o Simple --language C --debug-exception 2>&1
gcc  -I. ../lexer.c Simple/Simple.c -o lexer \
     -DPRINT_TOKEN \
     -DQUEX_OPTION_ASSERTS_WARNING_MESSAGE_DISABLED_EXT 2>&1 
./lexer


# cat tmp.txt | awk '(/[Ww][Aa][Rr][Nn][Ii][Nn][Gg]/ || /[Ee][Rr][Rr][Oo][Rr]/) && ! /ASSERTS/ '
rm -rf Simple*
rm -f ./lexer

# cleansening
cd $tmp

#! /usr/bin/env bash
if [[ $1 == "--hwut-info" ]]; then
    echo "Bad character detection.;"
    echo "CHOICES: default, customized, customized-2;"
    echo "HAPPY:   Simple/Simple.c:[0-9]+:;"
    exit
fi

if [[ $1 == "default" ]]; then
    buffer_size=7
else
    buffer_size=11
fi

quex -i src/bad-$1.qx -o Simple --language C --debug-exception
gcc -I. -I. -Wall -Werror                   \
    Simple/Simple.c lexer2nd.c -o lexer \
    -DPRINT_TOKEN                                    \
    -DQUEX_SETTING_BUFFER_SIZE=$buffer_size          \
    -DQUEX_OPTION_INFORMATIVE_BUFFER_OVERFLOW_MESSAGE -ggdb

#     -DQUEX_OPTION_DEBUG_SHOW 

if [[ $1 == "customized-2" ]]; then
    ./lexer data/bad2.txt > out.txt 2> err.txt
else
    ./lexer data/bad.txt > out.txt 2> err.txt
fi

cat out.txt err.txt

# echo "DEBUG: no deletion"
rm -rf ./EasyLexer* ./lexer out.txt err.txt

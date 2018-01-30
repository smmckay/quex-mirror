#! /usr/bin/env bash

function build_lexer {
    quex -i overflow-and-reallocate.qx -o EasyLexer --language C
    gcc $QUEX_PATH/demo/C/example.c EasyLexer.c  \
        -I. -I$QUEX_PATH \
        -DPRINT_TOKEN \
        -DQUEX_SETTING_BUFFER_SIZE=4 \
        -DQUEX_SETTING_BUFFER_FALLBACK_N=0 \
        -o lexer
    # -DQUEX_OPTION_DEBUG_SHOW -lefence -ggdb
}

case $1 in
    --hwut-info)
        echo "Provoque overflow and automatic buffer resize;"
        echo "CHOICES: plain, included;"
        echo "HAPPY: [0-9]+;"
        ;;

    plain)
        if [ "$2" == "FIRST" ] || [ -z "$2"  ]; then 
            build_lexer
        fi
        bash $QUEX_PATH/TEST/valgrind-executer.sh ./lexer \
                                                  data/overflow-and-reallocate.txt
        ;; 
    included)
        if [ "$2" == "FIRST" ] || [ -z "$2"  ]; then 
            build_lexer
        fi
        bash $QUEX_PATH/TEST/valgrind-executer.sh ./lexer \
                                                  data/overflow-and-reallocate-include-2.txt
        ;;
esac

if [ "$3" == "LAST" ] || [ -z "$3" ]; then 
    rm -f EasyLexer* lexer
fi

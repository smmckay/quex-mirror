#! /usr/bin/env bash
source $HWUT_PATH/support/bash/hwut_unit.sh

function build_lexer {
    quex -i overflow-and-reallocate.qx -o EHLexer --language C
    gcc lexer2nd.c EHLexer/EHLexer.c  \
        -I. -DPRINT_TOKEN \
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
        hwut_if_first $2 build_lexer
        bash $QUEX_PATH/TEST/valgrind-executer.sh ./lexer \
                                                  data/overflow-and-reallocate.txt
        ;; 
    included)
        hwut_if_first $2 build_lexer
        bash $QUEX_PATH/TEST/valgrind-executer.sh ./lexer \
                                                  data/overflow-and-reallocate-include-2.txt
        ;;
esac

hwut_if_last $3 "rm -rf EHLexer lexer"

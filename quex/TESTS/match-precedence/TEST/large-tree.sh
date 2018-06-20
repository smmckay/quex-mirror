#! /usr/bin/env bash
if [[ $1 == "--hwut-info" ]]; then
    echo "Precedence: Larger Inheritance Tree;"
    exit
fi
quex -i data/large-tree.qx -o Simple --token-id-prefix T_ --language C --debug-exception
gcc -I$QUEX_PATH -I. \
    -DQUEX_OPTION_ASSERTS_WARNING_MESSAGE_DISABLED_EXT \
    -DPRINT_LINE_COLUMN_NUMBER \
    -DPRINT_TOKEN \
    $QUEX_PATH/TEST/lexer.c Simple/Simple.c -o lexer  \
    -DQUEX_TKN_TERMINATION=T_TERMINATION
./lexer data/large-tree.txt
rm -rf ./lexer Simple*

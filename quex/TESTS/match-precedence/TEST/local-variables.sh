#! /usr/bin/env bash
if [[ $1 == "--hwut-info" ]]; then
    echo "Local variables."
    exit
fi

echo "Watch if the generated code compiles. If is 'ls lexer' succeeds."
quex -i data/local-variables.qx -o Simple --debug-exception
rm -f ./lexer
g++ -I$QUEX_PATH -I. \
    -DQUEX_OPTION_ASSERTS_WARNING_MESSAGE_DISABLED_EXT \
    $QUEX_PATH/TEST/lexer.cpp Simple/Simple.cpp -o lexer  
ls lexer
rm -rf ./lexer Simple
# rm -f Simple*

#! /usr/bin/env bash
if [[ $1 == "--hwut-info" ]]; then
    echo "Customized Event Handlers;"
    echo "CHOICES: bash, c, mix;"
    exit
fi


qx_file=src/comment.qx
txt_file=data/comment-$1.txt
buffer_size=25

if [[ "$*" == *"FIRST"* ]]; then
    quex -i $qx_file -o EasyLexer --language C --debug-exception
    gcc -ggdb \
        -I$QUEX_PATH -I.                                 \
        EasyLexer.c                                      \
        $QUEX_PATH/demo/C/example.c                      \
        -o lexer -DPRINT_TOKEN                           \
        -DQUEX_SETTING_BUFFER_SIZE=$buffer_size          \
        -DQUEX_OPTION_ASSERTS_WARNING_MESSAGE_DISABLED
fi


# -DQUEX_OPTION_DEBUG_SHOW 

./lexer $txt_file &> tmp.txt

cat tmp.txt

if [[ "$*" == *"LAST"* ]]; then
    rm -f ./EasyLexer*
    rm -f ./lexer
    rm -f tmp.txt
fi


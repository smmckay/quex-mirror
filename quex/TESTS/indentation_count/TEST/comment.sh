#! /usr/bin/env bash
if [[ $1 == "--hwut-info" ]]; then
    echo "Customized Event Handlers;"
    echo "CHOICES: bash, c, mix;"
    exit
fi


qx_file=src/comment.qx
txt_file=data/comment-$1.txt
buffer_size=25

if [ "$2" == "FIRST" ] || [ -z "$2"  ]; then 
    quex --cbm -i $qx_file -o Simple --language C --debug-exception
    gcc -ggdb \
        -I.                                              \
        Simple/Simple.c                                  \
        lexer2nd.c -o lexer -DPRINT_TOKEN                \
        -DQUEX_SETTING_BUFFER_SIZE_EXT=$buffer_size          \
        -DQUEX_OPTION_ASSERTS_WARNING_MESSAGE_DISABLED_EXT
fi


# -DQUEX_OPTION_DEBUG_SHOW_EXT 

./lexer $txt_file &> tmp.txt

cat tmp.txt

if [ "$3" == "LAST" ] || [ -z "$3" ]; then 
    rm -rf ./Simple* ./lexer tmp.txt
fi


#! /usr/bin/env bash
if [[ $1 == "--hwut-info" ]]; then
    echo "Customized Event Handlers;"
    echo "CHOICES: check-eof, on_dedent, on_n_dedent, empty-lines, on_indentation_error;"
    exit
fi


if [[ $1 == "on_dedent" ]]; then
    qx_file=src/handlers.qx
    txt_file=data/handlers.txt
    buffer_size=25
fi

if [[ $1 == "on_n_dedent" ]]; then
    qx_file=src/handlers-n.qx
    txt_file=data/handlers.txt
    buffer_size=25
fi

if [[ $1 == "check-eof" ]]; then
    qx_file=src/handlers-n.qx
    txt_file=data/null.txt
    buffer_size=8
fi

if [[ $1 == "empty-lines" ]]; then
    qx_file=src/handlers-n.qx
    txt_file=data/empty-lines.txt
    buffer_size=30
fi

if [[ $1 == "on_indentation_error" ]]; then
    qx_file=src/handlers.qx
    txt_file=data/on_indentation_error.txt
    buffer_size=30
fi
quex -i $qx_file -o Simple --language C --debug-exception

gcc \
    -I.                                              \
    Simple/Simple.c                                  \
    lexer2nd.c                                       \
    -o lexer -DPRINT_TOKEN                           \
    -DQUEX_SETTING_BUFFER_SIZE_EXT=$buffer_size          \
    -DQUEX_OPTION_ASSERTS_WARNING_MESSAGE_DISABLED_EXT

# -DQUEX_OPTION_DEBUG_SHOW_EXT 

./lexer $txt_file &> tmp.txt

cat tmp.txt

rm -f ./Simple* ./lexer tmp.txt


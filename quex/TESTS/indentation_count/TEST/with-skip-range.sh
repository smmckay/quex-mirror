#! /usr/bin/env bash
if [[ $1 == "--hwut-info" ]]; then
    echo "Indentation Counting and Range Skipper;"
    echo "CHOICES: range, range-2, nested_range;"
    exit
fi

qx_file=src/with-skip-$1.qx
txt_file=data/with-skip-$1.txt
buffer_size=1024

quex --cbm -i $qx_file -o Simple --language C --debug-exception

gcc \
 -ggdb -I.                                        \
 Simple/Simple.c                                  \
 lexer2nd.c                                       \
 -o lexer -DPRINT_TOKEN                           \
 -DQUEX_SETTING_BUFFER_SIZE_EXT=$buffer_size          \
 -DQUEX_OPTION_ASSERTS_WARNING_MESSAGE_DISABLED_EXT

./lexer $txt_file &> tmp.txt

cat tmp.txt

rm -rf ./Simple* ./lexer tmp.txt


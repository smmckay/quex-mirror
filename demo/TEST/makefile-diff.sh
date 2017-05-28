#! /usr/bin/env bash
if [[ $1 == "--hwut-info" ]]; then
    echo "Makefile Differences to C++ Version;"
    echo "CHOICES:  00-Minimalist, 01-Trivial, 02-ModesAndStuff, 03-Indentation, 04-ConvertersAndBOM, 05-LexerForC, 06-Include, 07-TrailingPostContext, 08-DeletionAndPriorityMark, 09-WithBisonParser, 10-SocketsAndTerminal, 11-ManualBufferFilling, 12-EngineEncoding, 13-MultipleLexers, 14-MultipleLexersSameToken;"
    exit
fi
diff --ignore-tab-expansion \
     --ignore-space-change  \
     --ignore-all-space     \
     --ignore-blank-lines   \
     $QUEX_PATH/demo/Cpp/$1/Makefile \
     $QUEX_PATH/demo/C/$1/Makefile | awk '! /[0-9]+[a-z]+[0-9]+/'
     # --ignore-matching-lines=RE

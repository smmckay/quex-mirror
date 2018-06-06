#! /usr/bin/env bash

case $1 in
    --hwut-info)
        echo "Test code comments;"
        echo "HAPPY: [0-9]+;"
        ;;

    *)
        quex -i comment.qx --odir WithOut 
        quex -i comment.qx --odir With   \
             --comment-state-machine \
             --comment-mode-patterns \
             --comment-transitions   \
             --debug-exception
        # awk NF => print only non-empty lines
        grep -ve '^# *line' With/Lexer.cpp    | awk NF > tmp1.txt
        grep -ve '^# *line' WithOut/Lexer.cpp | awk NF > tmp2.txt
        diff tmp1.txt tmp2.txt | grep '^ *<'
        rm -rf With* tmp1.txt tmp2.txt
        ;;
esac

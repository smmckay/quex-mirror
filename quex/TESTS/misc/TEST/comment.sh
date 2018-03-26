#! /usr/bin/env bash

case $1 in
    --hwut-info)
        echo "Test code comments;"
        echo "HAPPY: [0-9]+;"
        ;;

    *)
        quex -i comment.qx -o WithOut 
        quex -i comment.qx -o With   \
             --comment-state-machine \
             --comment-mode-patterns \
             --comment-transitions   \
             --debug-exception
        diff With/With.cpp WithOut/WithOut.cpp | awk ' (/</ || />/) && ! /\#/ '
        rm -rf With*
        ;;
esac

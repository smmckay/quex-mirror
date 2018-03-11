#! /usr/bin/env bash
source ../../TEST/build-and-run.sh

hwut_info $1 \
    "02-ModesAndStuff: Multiple Modes, Mode Transitions;" \
    "CHOICES:  asserts, no-asserts;"                      \
    "SAME;"

directory="../02-ModesAndStuff"
choice=$1

pushd $directory >& /dev/null

# Clean always, because there is w/ and wo/ 'asserts'
bar_clean 
bar_build lexer "$choice" 
bar_run   lexer 
bar_clean 

popd >& /dev/null


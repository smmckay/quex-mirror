#! /usr/bin/env bash
source ../../Cpp/TEST/build-and-run.sh

hwut_info $1 \
    "demo/001: Multiple Modes, Mode Transitions" \
    "CHOICES:  asserts, no-asserts;"             \
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


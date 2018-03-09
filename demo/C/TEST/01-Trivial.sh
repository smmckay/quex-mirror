#! /usr/bin/env bash
source build-and-run.sh

hwut_info $1 \
    "01-Trivial: Single Mode Example;\n" \
    "CHOICES:  asserts, no-asserts;\n"  \
    "SAME;\n"

directory="../01-Trivial"
choice=$1

pushd $directory >& /dev/null

# Clean always, because there is w/ and wo/ 'asserts'
bar_clean 
bar_build lexer "$choice" 
bar_run   lexer 
bar_clean 

popd >& /dev/null

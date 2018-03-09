#! /usr/bin/env bash
source $HWUT_PATH/support/bash/hwut_unit.sh
hwut_info $1 \
    "01-Trivial: Single Mode Example;\n" \
    "CHOICES:  asserts, no-asserts;\n"  \
    "SAME;\n"

directory="../01-Trivial"
choice=$2
first_f=$3
last_f=$4

source build-and-run.sh

pushd $directory >& /dev/null

build lexer $choice "$first_f"
run   lexer 
clean "$last_f"

popd >& /dev/null

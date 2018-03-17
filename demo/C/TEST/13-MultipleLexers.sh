#! /usr/bin/env bash
source ../../TEST/build-and-run.sh

hwut_info $1 \
    "13-MultipleLexers: Single Application/Multiple Lexical Analyzers;\n" \
    "CHOICES:  asserts, no-asserts;\n"                           \
    "SAME;"

choice=$1

bar_build_always_and_run "../13-MultipleLexers" lexer "$choice"


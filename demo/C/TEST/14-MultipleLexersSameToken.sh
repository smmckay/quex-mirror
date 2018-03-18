#! /usr/bin/env bash
source ../../TEST/build-and-run.sh

hwut_info $1 \
    "14-MultipleLexersSameToken: Multiple Lexical Analyzers -- shared token;\n" \
    "CHOICES:  asserts, no-asserts;\n"                                          \
    "SAME;"

choice=$1

bar_build_always_and_run "../14-MultipleLexersSameToken" lexer "$choice"

#! /usr/bin/env bash
source ../../TEST/build-and-run.sh

hwut_info $1 \
    "05-LexerForC: A C-Lexical Analyser;\n" \
    "CHOICES:  NDEBUG, DEBUG;\n"        \
    "SAME;"

choice=$1

bar_build_always_and_run "../05-LexerForC" lexer "$choice"


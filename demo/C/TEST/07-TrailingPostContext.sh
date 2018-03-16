#! /usr/bin/env bash
source ../../TEST/build-and-run.sh

hwut_info $1 \
    "demo/006: Pseudo Ambiguous Post Conditions;\n" \
    "CHOICES:  asserts, no-asserts;\n"  \
    "SAME;"

choice=$1

bar_build_always_and_run "../07-TrailingPostContext" lexer "$choice"

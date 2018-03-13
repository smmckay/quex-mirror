#! /usr/bin/env bash
source ../../TEST/build-and-run.sh

hwut_info $1 \
    "01-Trivial: Single Mode Example;\n" \
    "CHOICES:  asserts, no-asserts;\n"  \
    "SAME;\n"

choice=$1

bar_build_always_and_run "../01-Trivial" lexer "$choice"

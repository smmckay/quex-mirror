#! /usr/bin/env bash
source ../../TEST/build-and-run.sh

hwut_info $1 \
    "09-WithBisonParser: Linking Lexical Analysis to Bison Parser;\n" \
    "CHOICES:  asserts, no-asserts;\n"                                \
    "SAME;"

bar_build_always_and_run "../09-WithBisonParser" parser "$1"

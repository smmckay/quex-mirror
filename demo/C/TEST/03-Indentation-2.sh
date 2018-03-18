#! /usr/bin/env bash
source ../../TEST/build-and-run.sh

hwut_info $1 \
    "03-Indentation: Off-side rule (second case);" \
    "CHOICES:  asserts, no-asserts;" \
    "SAME;"

choice=$1

bar_build_always_and_run "../03-Indentation" lexer2 "$choice" example2.txt


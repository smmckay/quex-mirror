#! /usr/bin/env bash
source ../../TEST/build-and-run.sh

hwut_info $1 \
    "02-ModesAndStuff: Multiple Modes, Mode Transitions;" \
    "CHOICES:  asserts, no-asserts;"                      \
    "SAME;"

choice=$1

bar_build_always_and_run "../02-ModesAndStuff" lexer "$choice"


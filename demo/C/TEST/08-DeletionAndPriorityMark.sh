#! /usr/bin/env bash
source ../../TEST/build-and-run.sh

hwut_info $1 \
    "08-DeletionAndPriorityMark: Priorization;\n" 

bar_build_always_and_run "../08-DeletionAndPriorityMark" lexer ""

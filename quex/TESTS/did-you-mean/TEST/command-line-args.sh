#! /usr/bin/env bash
if [[ $1 == "--hwut-info" ]]; then
    echo "Command line arguments;"
    exit
fi

quex --config-by-gmake
quex --helpy

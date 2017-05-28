#! /usr/bin/env bash
if [[ $1 == "--hwut-info" ]]; then
    echo "demo/012: Single Application/Multiple Lexical Analyzers"
    echo "CHOICES:  NDEBUG, DEBUG;"
    echo "SAME;"
    exit
fi
cp 012-side-kick.sh side-kick.sh
source core-new.sh 13-MultipleLexers $2 $3 $1

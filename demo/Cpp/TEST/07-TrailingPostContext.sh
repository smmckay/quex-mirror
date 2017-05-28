#! /usr/bin/env bash
if [[ $1 == "--hwut-info" ]]; then
    echo "demo/006: Pseudo Ambiguous Post Conditions"
    echo "CHOICES:  NDEBUG, DEBUG;"
    echo "SAME;"
    exit
fi
cp 07-TrailingPostContext-side-kick.sh side-kick.sh
source core-new.sh 07-TrailingPostContext $2 $3 $1

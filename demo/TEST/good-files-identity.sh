#! /usr/bin/env bash
if [[ "$1" == "--hwut-info" ]]; then
    echo "List all GOOD files which are identical;"
    exit
fi

pushd ../C/TEST/GOOD > /dev/null

for file in *.txt; do 
    diff -srq $file ../../../Cpp/TEST/GOOD/$file
done 2>/dev/null \
  | awk '/identical/ { print $2; }' \
  | sort

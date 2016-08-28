#! /usr/bin/env bash
if [[ $1 == "--hwut-info" ]]; then
    echo "No references to C demos;"
    exit
fi

echo
echo "-- Check for references to 'C demos' (no output is good output) --"
grep -sHIne '/C/' *.sh | awk '! /no-references/'
echo "--"
echo
echo "-- Check for references to 'Cpp demos' --"
grep -sHIne '/Cpp/' *.sh | sort | awk '! /no-references/'
echo "--"
echo "<terminated>"

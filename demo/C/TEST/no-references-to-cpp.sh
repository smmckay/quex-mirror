#! /usr/bin/env bash
if [[ $1 == "--hwut-info" ]]; then
    echo "No references to Cpp demos;"
    exit
fi

echo
echo "-- Check for references to 'Cpp demos' (no output is good output) --"
echo "||||"
grep -sHIne '/Cpp/' *.sh | awk '! /no-references/ && ! /makefile-diff/'
echo "||||"
echo "--"
echo
echo "-- Check for references to 'Cpp demos' --"
echo "||||"
grep -sHIne '/C/' *.sh | awk '! /no-references/ && ! /makefile-diff/'
echo "||||"
echo "--"
echo "<terminated>"

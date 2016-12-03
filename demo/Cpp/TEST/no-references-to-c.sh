#! /usr/bin/env bash
if [[ $1 == "--hwut-info" ]]; then
    echo "No references to C demos;"
    exit
fi

echo
echo "-- Check for references to 'C demos' (no output is good output) --"
echo "||||"
grep -sHIne '/C/' *.sh | awk '! /no-references/' 
echo "||||"
echo "--"
echo
echo "-- Check for references to 'Cpp demos' --"
echo "||||"
grep -sHIne '/Cpp/' *.sh | sort | awk '! /no-references/' 
echo "||||"
echo "--"
echo "<terminated>"
